import logging
import os
from ast import AST, AsyncFunctionDef, FunctionDef, Import, ImportFrom
from ast import parse as pyast_parse
from ast import unparse as pyast_unparse
from ast import walk as pyast_walk
from contextlib import contextmanager
from typing import List, Optional, Set, Union

import tiktoken

from automata.core.base.database.vector import VectorDatabaseProvider
from automata.core.utils import get_docstring_from_node, get_root_py_fpath
from automata.symbol.base import Symbol
from automata.symbol.graph import SymbolGraph
from automata.symbol.symbol_utils import (
    get_rankable_symbols,
    get_source_code_of_symbol_using_py_ast,
)

logger = logging.getLogger(__name__)


class PyContextRetrieverConfig:
    """The configuration for the PyContextRetriever"""

    def __init__(
        self,
        spacer: str = "  ",
        max_dependencies_to_process: int = 10,
        max_related_symbols_to_process: int = 10,
        max_context: int = 6_500,
    ) -> None:
        self.spacer = spacer
        self.max_dependencies_to_process = max_dependencies_to_process
        self.max_related_symbols_to_process = max_related_symbols_to_process
        self.max_context = max_context


class PyContextRetriever:
    """The PyContextRetriever is used to retrieve the context of a symbol in a Python project"""

    def __init__(
        self,
        graph: SymbolGraph,
        config: PyContextRetrieverConfig = PyContextRetrieverConfig(),
        doc_embedding_db: Optional[VectorDatabaseProvider] = None,
        encoding_provider: tiktoken.Encoding = tiktoken.encoding_for_model("gpt-4"),
    ) -> None:
        self.graph = graph
        self.config = config
        self.indent_level = 0
        self.doc_embedding_db = doc_embedding_db
        self.encoding_provider = encoding_provider

        self.reset()

    @contextmanager
    def IndentManager(self):
        self.indent_level += 1
        yield
        self.indent_level -= 1

    def process_message(self, message: str):
        def indent() -> str:
            return self.config.spacer * self.indent_level

        self.context += "\n".join([f"{indent()}{ele}" for ele in message.split("\n")]) + "\n"

    def get_context_buffer(self) -> str:
        return self.context

    def reset(self) -> None:
        self.context = ""
        self.obs_symbols: Set[Symbol] = set([])
        self.global_level = 0

    def process_symbol(
        self,
        symbol: Symbol,
        related_symbols: List[Symbol] = [],
    ) -> None:  # sourcery skip: extract-method
        """
        Process the context of a specified `Symbol`.

        This works by first processing the main printout for the symbol, which includes the symbol's
        documentation, docstring, and methods. Then, if the symbol is the main symbol, we process
        the context for the symbol's related symbols and dependencies.

        """
        with self.IndentManager():
            self.process_headline(symbol)
            self.process_ast(symbol)

            if self._is_main_symbol():
                related_symbols_processed = 0
                self.process_message(f"Building context for related symbols -\n")

                for related_symbol in related_symbols:
                    if related_symbols_processed >= self.config.max_related_symbols_to_process:
                        break

                    # Check that the related symbol passes filter requirements
                    if not PyContextRetriever._pass_symbol_filter(symbol, related_symbol):
                        continue

                    if not self._below_context_limit():
                        break

                    if related_symbol not in self.obs_symbols:
                        self.process_symbol(related_symbol)
                        related_symbols_processed += 1

                dependencies_processed = 0
                self.process_message(f"Building context for dependencies -\n")
                all_dependencies = list(self.graph.get_symbol_dependencies(symbol))
                filtered_dependencies = get_rankable_symbols(all_dependencies)

                for dependency in filtered_dependencies:
                    if dependencies_processed >= self.config.max_dependencies_to_process:
                        break

                    # Check that the dependency passes filter requirements
                    if not PyContextRetriever._pass_symbol_filter(symbol, dependency):
                        continue

                    if not self._below_context_limit():
                        break

                    if dependency not in self.obs_symbols:
                        try:
                            self.process_symbol(dependency)
                        except Exception as e:
                            logger.error(f"Failure processing dependent {dependency} with {e}")
                            continue
                        dependencies_processed += 1

        self.obs_symbols.add(symbol)

    def process_headline(self, symbol: Symbol) -> None:
        # Print the headline
        if self._is_main_symbol():
            self.process_message(f"Building context for primary symbol - {symbol.dotpath} -\n")
        else:
            self.process_message(f"{symbol.dotpath}\n")

    def process_ast(self, symbol: Symbol) -> None:
        """Process the entire context for an AST object."""
        ast_object = get_source_code_of_symbol_using_py_ast(symbol)
        is_main_symbol = self._is_main_symbol()
        methods = sorted(PyContextRetriever._get_all_methods(ast_object), key=lambda x: x.name)

        with self.IndentManager():
            if "test" in symbol.dotpath or "Config" in symbol.dotpath:
                with self.IndentManager():
                    self.process_message(f"{pyast_unparse(ast_object)}\n")
            else:
                if is_main_symbol:
                    self.process_imports(symbol)
                self.process_documentation(symbol, is_main_symbol)

                self.process_docstring(ast_object)

                if len(methods) > 0:
                    self.process_message("Methods:")
                for method in methods:
                    self.process_method(method, is_main_symbol)

    def process_imports(self, symbol: Symbol) -> None:
        """Appends the import statements for a symbol to the context buffer."""
        # Compute the file path from the symbol's path
        file_path = os.path.join(
            get_root_py_fpath(), "..", str(symbol.dotpath).replace(".", os.path.sep)
        )
        while not os.path.isdir(os.path.dirname(file_path)):
            file_path = os.path.dirname(file_path)

        # Load the source code with AST
        with open(f"{file_path}.py", "r") as f:
            ast = pyast_parse(f.read())

        # Find and print import statements
        imports = PyContextRetriever._get_all_imports(ast)
        if len(imports) > 0:
            self.process_message("Import Statements:")
            with self.IndentManager():
                for import_node in imports:
                    self.process_message(pyast_unparse(import_node))
                self.process_message("")  # Add an empty line for separation

    def process_docstring(self, ast_object: AST) -> None:
        docstring = PyContextRetriever._get_docstring(ast_object)

        if docstring:
            self.process_message("Class Docstring:")
            with self.IndentManager():
                self.process_message(docstring)
                self.process_message("")  # Add an empty line for separation

    def process_documentation(self, symbol: Symbol, is_main_symbol: bool) -> None:
        """
        Process the documentation of a symbol, providing a summary or the entire source code
        depending on whether the symbol is the main symbol or not.
        """

        if self.doc_embedding_db is not None and self.doc_embedding_db.contains(symbol.dotpath):
            if is_main_symbol:
                document = self.doc_embedding_db.get(symbol.dotpath).document
            else:
                document = self.doc_embedding_db.get(symbol.dotpath).summary
            self.process_message("Class Document:")
            with self.IndentManager():
                self.process_message(document)
                self.process_message("")  # Add an empty line for separation

    def process_method(
        self, method: Union[AsyncFunctionDef, FunctionDef], is_main_symbol: bool
    ) -> None:
        """
        Processes a specified method by printing its name, arguments, and return type.
        If we are processing the main symbol, we also print the method's code.
        """
        if PyContextRetriever._is_private_method(method):
            return
        with self.IndentManager():
            if not is_main_symbol and method.name == "__init__" or is_main_symbol:
                for code_line in pyast_unparse(method).split("\n"):
                    self.process_message(code_line)
            else:
                method_definition = (
                    f"{method.name}({PyContextRetriever._get_method_arguments(method)})"
                )
                return_annotation = PyContextRetriever._get_method_return_annotation(method)
                self.process_message(f"{method_definition} -> {return_annotation}\n")

    def _is_main_symbol(self) -> bool:
        return self.indent_level == 1

    def _below_context_limit(self) -> bool:
        return len(self.encoding_provider.encode(self.context)) < self.config.max_context

    @staticmethod
    def _get_method_arguments(method: Union[AsyncFunctionDef, FunctionDef]) -> str:
        return ", ".join([arg.arg for arg in method.args.args])

    @staticmethod
    def _get_method_return_annotation(method: Union[AsyncFunctionDef, FunctionDef]) -> str:
        return_annotation = None
        if method.returns is not None:
            return_annotation = pyast_unparse(method.returns)
            return return_annotation
        return "None"

    @staticmethod
    def _is_private_method(ast_object: Union[AsyncFunctionDef, FunctionDef]) -> bool:
        return ast_object.name[0] == "_" and ast_object.name[1] != "_"

    @staticmethod
    def _get_docstring(ast_object: AST) -> str:
        raw_doctring = get_docstring_from_node(ast_object).split("\n")
        return "\n".join([ele.strip() for ele in raw_doctring]).strip()

    @staticmethod
    def _pass_symbol_filter(primary_symbol: Symbol, secondary_symbol: Symbol) -> bool:
        primary_symbol_dotpath = primary_symbol.dotpath
        primary_package = primary_symbol_dotpath.split(".")[0]

        secondary_symbol_dotpath = secondary_symbol.dotpath
        secondary_package = secondary_symbol_dotpath.split(".")[0]
        return not (
            primary_symbol_dotpath in secondary_symbol_dotpath
            or primary_package != secondary_package
        )

    @staticmethod
    def _get_all_imports(ast: AST):
        imports: List[Union[Import, ImportFrom]] = []
        for node in pyast_walk(ast):
            if isinstance(node, Import):
                imports.append(node)
            elif isinstance(node, ImportFrom):
                imports.append(node)
        return imports

    @staticmethod
    def _get_all_methods(ast: AST):
        methods: List[Union[FunctionDef, AsyncFunctionDef]] = []
        for node in pyast_walk(ast):
            if isinstance(node, FunctionDef):
                methods.append(node)
            elif isinstance(node, AsyncFunctionDef):
                methods.append(node)
        return methods
