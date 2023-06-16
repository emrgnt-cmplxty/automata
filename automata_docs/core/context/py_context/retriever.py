import logging
import os
from contextlib import contextmanager
from typing import List, Optional, Set

import tiktoken
from redbaron import RedBaron

from automata_docs.core.coding.py_coding.retriever import PyCodeRetriever
from automata_docs.core.database.vector import VectorDatabaseProvider
from automata_docs.core.symbol.graph import SymbolGraph
from automata_docs.core.symbol.symbol_types import Symbol
from automata_docs.core.symbol.symbol_utils import convert_to_fst_object, get_rankable_symbols
from automata_docs.core.utils import root_py_fpath

logger = logging.getLogger(__name__)


class PyContextRetrieverConfig:
    """The configuration for the PyContextRetriever"""

    def __init__(
        self,
        spacer: str = "  ",
        max_dependencies_to_process: int = 10,
        max_related_symbols_to_process: int = 10,
        model_name: str = "gpt-4",
        max_context: int = 6_500,
    ):
        """
        Args:
            spacer (str): The string to use for indentation
            max_dependency_print_depth (int): The maximum depth to print dependencies
            max_recursion_depth (int): The maximum depth to recurse into dependencies
            max_related_symbols_to_process (int): The number of nearest symbols to print
        """
        self.spacer = spacer
        self.max_dependencies_to_process = max_dependencies_to_process
        self.max_related_symbols_to_process = max_related_symbols_to_process
        self.model_name = model_name
        self.max_context = max_context


class PyContextRetriever:
    """The PyContextRetriever is used to retrieve the context of a symbol in a Python project"""

    def __init__(
        self,
        graph: SymbolGraph,
        config: PyContextRetrieverConfig = PyContextRetrieverConfig(),
        doc_embedding_db: Optional[VectorDatabaseProvider] = None,
    ):
        """
        Args:
            graph (SymbolGraph): The symbol graph to use
            config (PyContextRetrieverConfig): The configuration to use
        """
        self.graph = graph
        self.config = config
        self.indent_level = 0
        self.doc_embedding_db = doc_embedding_db
        self.encoding = tiktoken.encoding_for_model(self.config.model_name)

        self.reset()

    @contextmanager
    def IndentManager(self):
        """A context manager to manage the indentation level"""
        self.indent_level += 1
        yield
        self.indent_level -= 1

    def process_message(self, message: str):
        """
        Process a message by appending indentation and adding it to the message

        Args:
            message (str): The message to process
        """

        def indent() -> str:
            return self.config.spacer * self.indent_level

        self.context += "\n".join([f"{indent()}{ele}" for ele in message.split("\n")]) + "\n"

    def get_context_buffer(self) -> str:
        """
        Get the context buffer

        Returns:
            str: The context buffer
        """
        return self.context

    def reset(self):
        """
        Reset the retriever to its initial state
        """
        self.context = ""
        self.obs_symbols: Set[Symbol] = set([])
        self.global_level = 0

    def process_symbol(
        self,
        symbol: Symbol,
        related_symbols: List[Symbol] = [],
    ):
        """
        Process the context of a symbol
        Theh output is stored into the local message buffer

        Args:
            symbol (Symbol): The symbol to process
            ranked_symbols (List[Symbol]): The list ranked symbols to use
                with the nearest symbol processor
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

    def process_headline(self, symbol: Symbol):
        """
        Process the headline of a symbol

        Args:
            symbol (Symbol): The symbol to process
        """
        # Print the headline
        if self._is_main_symbol():
            self.process_message(f"Building context for primary symbol - {symbol.dotpath} -\n")
        else:
            self.process_message(f"{symbol.dotpath}\n")

    def process_ast(self, symbol: Symbol):
        """
        Process the variables of a symbol

        Args:
            ast_object (RedBaron): The ast representation of the symbol
        """
        ast_object = convert_to_fst_object(symbol)
        is_main_symbol = self._is_main_symbol()
        methods = sorted(ast_object.find_all("DefNode"), key=lambda x: x.name)

        with self.IndentManager():
            if "test" in symbol.dotpath or "Config" in symbol.dotpath:
                with self.IndentManager():
                    self.process_message(f"{ast_object.dumps()}\n")
            else:
                if is_main_symbol:
                    self.process_imports(symbol)
                self.process_documentation(symbol, is_main_symbol)

                self.process_docstring(ast_object)

                if len(methods) > 0:
                    self.process_message(f"Methods:")
                for method in methods:
                    self.process_method(method, is_main_symbol)

    def process_imports(self, symbol: Symbol):
        """
        Process the imports of a symbol

        Args:
            symbol (Symbol): The symbol to process
        """
        # Compute the file path from the symbol's path
        file_path = os.path.join(
            root_py_fpath(), "..", str(symbol.dotpath).replace(".", os.path.sep)
        )
        while not os.path.isdir(os.path.dirname(file_path)):
            file_path = os.path.dirname(file_path)

        # Load the source code with RedBaron
        with open(file_path + ".py", "r") as f:
            red = RedBaron(f.read())

        # Find and print import statements
        imports = red.find_all("ImportNode")
        from_imports = red.find_all("FromImportNode")
        if len(imports) + len(from_imports) > 0:
            self.process_message("Import Statements:")
            with self.IndentManager():
                for import_node in imports + from_imports:
                    self.process_message(str(import_node.dumps()))
                self.process_message("")  # Add an empty line for separation

    def process_docstring(self, ast_object: RedBaron):
        """
        Process the docstring of a symbol

        Args:
            ast_object (RedBaron): The ast representation of the symbol
        """
        docstring = PyContextRetriever._get_docstring(ast_object)
        # Print the docstring if it exists
        if docstring:
            self.process_message("Class Docstring:")
            with self.IndentManager():
                self.process_message(docstring)
                self.process_message("")  # Add an empty line for separation

    def process_documentation(self, symbol: Symbol, is_main_symbol: bool):
        if self.doc_embedding_db is not None:
            if self.doc_embedding_db.contains(symbol):
                if is_main_symbol:
                    document = self.doc_embedding_db.get(symbol).embedding_source
                else:
                    document = self.doc_embedding_db.get(symbol).summary
                with self.IndentManager():
                    self.process_message(document)
                    self.process_message("")  # Add an empty line for separation

    def process_method(self, method: RedBaron, is_main_symbol: bool):
        """
        Processes a specified method

        Args:
            method (RedBaron): The ast representation of the method
        """
        if PyContextRetriever._is_private_method(method):
            return
        with self.IndentManager():
            if is_main_symbol:
                for code_line in method.dumps().split("\n"):
                    self.process_message(code_line)
            else:
                if method.name == "__init__":
                    for code_line in method.dumps().split("\n"):
                        self.process_message(code_line)
                else:
                    method_definition = f"{method.name}({method.arguments.dumps()})"
                    return_annotation = (
                        method.return_annotation.dumps() if method.return_annotation else "None"
                    )
                    self.process_message(f"{method_definition} -> {return_annotation}\n")

    def _is_main_symbol(self) -> bool:
        """
        Check if this is the main symbol call

        Returns:
            bool: True if this is the main symbol call, False otherwise

        """
        return self.indent_level == 1

    def _below_context_limit(self) -> bool:
        """
        Check if we are below the context limit

        Returns:
            bool: True if we are below the context limit, False otherwise
        """
        return len(self.encoding.encode(self.context)) < self.config.max_context

    @staticmethod
    def _is_private_method(ast_object: RedBaron) -> bool:
        """
        Check if the ast object is private

        Args:
            ast_object (RedBaron): The RedBaron object to check

        Returns:
            bool: True if the method is private, False otherwise
        """
        return ast_object.name[0] == "_" and ast_object.name[1] != "_"

    @staticmethod
    def _get_docstring(ast_object) -> str:
        """
        Get the docstring an ast object

        Args:
            ast_object (RedBaron): The RedBaron object to get the docstring from

        Returns:
            str: Newline separated docstring
        """

        raw_doctring = PyCodeRetriever.get_docstring_from_node(ast_object).split("\n")
        return "\n".join([ele.strip() for ele in raw_doctring]).strip()

    @staticmethod
    def _pass_symbol_filter(primary_symbol: Symbol, secondary_symbol: Symbol) -> bool:
        """
        Check if the symbol passes the filter on package and dotpath

        Args:
            primary_symbol (Symbol): The primary symbol
            secondary_symbol (Symbol): The secondary symbol

        Returns:
            bool: True if the symbol passes the filter, False otherwise
        """

        primary_symbol_dotpath = primary_symbol.dotpath
        primary_package = primary_symbol_dotpath.split(".")[0]

        secondary_symbol_dotpath = secondary_symbol.dotpath
        secondary_package = secondary_symbol_dotpath.split(".")[0]
        return not (
            primary_symbol_dotpath in secondary_symbol_dotpath
            or primary_package != secondary_package
        )
