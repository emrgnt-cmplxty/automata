import logging
import os
from ast import AST, AsyncFunctionDef, ClassDef, FunctionDef, Import, ImportFrom
from ast import parse as py_ast_parse
from ast import unparse, walk
from contextlib import contextmanager
from enum import Enum
from typing import TYPE_CHECKING, Callable, Dict, List, Optional, Set, Union

import tiktoken

from automata.code_parsers.py import (
    get_docstring_from_node,
    get_node_without_docstrings,
    get_node_without_imports,
)
from automata.core.base import VectorDatabaseProvider
from automata.core.utils import get_root_py_fpath
from automata.symbol import Symbol

if TYPE_CHECKING:
    from automata.symbol import SymbolGraph

logger = logging.getLogger(__name__)


class PyContextRetrieverConfig:
    """The configuration for the PyContextRetriever"""

    def __init__(
        self,
        indent_level: int = 0,
        spacer: str = "  ",
    ) -> None:
        self.indent_level = indent_level
        self.spacer = spacer


class ContextComponent(Enum):
    HEADLINE = "headline"
    SOURCE_CODE = "source_code"
    INTERFACE = "interface"


class PyContextRetriever:
    """The PyContextRetriever is used to retrieve the context of a symbol in a Python project"""

    MAX_RECURSION_DEPTH = 2

    def __init__(
        self,
        config: PyContextRetrieverConfig = PyContextRetrieverConfig(),
        process_entry: Optional[Callable[[str], str]] = None,
    ) -> None:
        self.spacer = config.spacer
        self.indent_level = config.indent_level
        self.process_entry = (
            process_entry if process_entry is not None else self._default_process_entry
        )
        self.context_components = {
            ContextComponent.HEADLINE: self._process_headline,
            ContextComponent.SOURCE_CODE: self._source_code,
            ContextComponent.INTERFACE: self._interface,
        }

    @contextmanager
    def increased_indentation(self):
        self.indent_level += 1
        yield
        self.indent_level -= 1

    def _default_process_entry(self, message: str) -> str:
        spacer = self.spacer * self.indent_level
        indented_lines = [
            f"{spacer}{line}" if line.strip() else line for line in message.split("\n")
        ]
        return "\n".join(indented_lines) + "\n"

    def process_symbol(
        self,
        symbol: Symbol,
        ordered_active_components: Optional[Dict[ContextComponent, Dict]] = None,
    ) -> str:
        """
        Process the context of a specified `Symbol`. The caller has the responsibility
        to decide the indent level and context components to be processed.
        """
        from automata.symbol import convert_to_ast_object

        ast_object = convert_to_ast_object(symbol)

        if {ContextComponent.INTERFACE, ContextComponent.SOURCE_CODE}.issubset(
            ordered_active_components.keys()
        ):
            raise ValueError("Cannot retrieve both INTERFACE and SOURCE_CODE at the same time.")
        context = ""
        for component, kwargs in ordered_active_components.items():
            if component in self.context_components:
                context += self.process_entry(
                    self.context_components[component](symbol, ast_object, **kwargs)
                )
            else:
                logger.warn(f"Warning: {component} is not a valid context component.")
        return context

    def _process_headline(
        self,
        symbol: Symbol,
        ast_object: AST,
        headline_prefix="Building context for symbol - ",
        *args,
        **kwargs,
    ) -> str:
        """Convert a symbol into a headline."""
        return f"{headline_prefix}{symbol.dotpath}\n"

    def _source_code(
        self,
        symbol: Symbol,
        ast_object: AST,
        remove_imports: bool = True,
        remove_docstrings: bool = False,
        max_length: Optional[int] = None,
        *args,
        **kwargs,
    ) -> str:
        """Convert a symbol into underlying source code."""

        if remove_docstrings:
            ast_object = get_node_without_docstrings(ast_object)

        if remove_imports:
            ast_object = get_node_without_imports(ast_object)

        source = unparse(ast_object)

        return source[:max_length] if max_length else source

    def _interface(
        self,
        symbol: Optional[Symbol],
        ast_object: AST,
        skip_private: bool = True,
        include_docstrings: bool = True,
        header: str = "Interface:\n\n",
        class_header: str = "class ",
        recursion_depth: int = 0,
        *args,
        **kwargs,
    ) -> str:
        """Convert a symbol into an interface, skipping 'private' methods/classes if indicated."""
        if recursion_depth > self.MAX_RECURSION_DEPTH:
            raise RecursionError(f"Max recursion depth of {self.MAX_RECURSION_DEPTH} exceeded.")

        # indent according to indent_level
        interface = self.process_entry(header)

        if include_docstrings:
            interface += self.process_entry(get_docstring_from_node(ast_object) + "\n")

        classes = self._get_all_classes(ast_object)
        with self.increased_indentation():
            for cls in classes:
                decorators = [f"@{unparse(dec)}" for dec in cls.decorator_list]
                class_header = f"\{class_header}{cls.name}:\n\n"
                class_header = "\n".join(decorators + [class_header])
                interface += self._interface(
                    None,
                    cls,
                    skip_private,
                    include_docstrings,
                    header,
                    class_header,
                    recursion_depth=recursion_depth + 1,
                )

        methods = sorted(self._get_all_methods(ast_object), key=lambda x: x.name)
        for method in methods:
            if not skip_private or not self._is_private_method(method):
                interface += self.process_entry(self._process_method(method))
                if include_docstrings:
                    interface += self.process_entry(get_docstring_from_node(method) + "\n")

        return interface

    def _is_private_method(self, method: Union[AsyncFunctionDef, FunctionDef]) -> bool:
        """Checks if a method is private, i.e., starts with '_'."""
        return method.name.startswith("_")

    def _process_method(self, method: Union[AsyncFunctionDef, FunctionDef]) -> str:
        """
        Processes a specified method by printing its name, arguments, and return type.
        If we are processing the main symbol, we also print the method's code.
        """
        decorators = [f"@{unparse(dec)}" for dec in method.decorator_list]
        method_definition = f"{method.name}({self._get_method_arguments(method)})"
        return_annotation = self._get_method_return_annotation(method)
        return "\n".join(decorators + [f"{method_definition} -> {return_annotation}\n"])

    @staticmethod
    def _get_method_return_annotation(method: Union[AsyncFunctionDef, FunctionDef]) -> str:
        return unparse(method.returns) if method.returns is not None else "None"

    @staticmethod
    def _get_all_methods(ast: AST) -> List[Union[FunctionDef, AsyncFunctionDef]]:
        return [node for node in walk(ast) if isinstance(node, (FunctionDef, AsyncFunctionDef))]

    @staticmethod
    def _get_all_classes(ast: AST) -> List[ClassDef]:
        return [node for node in walk(ast) if isinstance(node, ClassDef)]

    @staticmethod
    def _get_method_arguments(method: Union[AsyncFunctionDef, FunctionDef]) -> str:
        args = []
        defaults = dict(
            zip(
                [arg.arg for arg in reversed(method.args.defaults)], reversed(method.args.defaults)
            )
        )

        for arg in method.args.args:
            if arg.arg in defaults:
                args.append(f"{arg.arg}={unparse(defaults[arg.arg])}")
            else:
                args.append(arg.arg)

        # Handle keyword-only arguments
        if method.args.kwonlyargs:
            for kwarg in method.args.kwonlyargs:
                default = next(
                    (
                        kw_default
                        for kw_default, kw_arg in zip(
                            method.args.kw_defaults, method.args.kwonlyargs
                        )
                        if kw_arg.arg == kwarg.arg
                    ),
                    None,
                )

                if default is not None:
                    args.append(f"{kwarg.arg}={unparse(default)}")
                else:
                    args.append(kwarg.arg)

        return ", ".join(args)

    # @staticmethod
    # def _get_method_arguments(method: Union[AsyncFunctionDef, FunctionDef]) -> str:
    #     return ", ".join([arg.arg for arg in method.args.args])

    # def process_message(self, message: str):
    #     def indent() -> str:
    #         return self.config.spacer * self.indent_level

    #     self.context += "\n".join([f"{indent()}{ele}" for ele in message.split("\n")]) + "\n"

    # def get_context_buffer(self) -> str:
    #     return self.context

    # def process_symbol(
    #     self,
    #     symbol: Symbol,
    #     related_symbols: List[Symbol] = [],
    # ) -> None:  # sourcery skip: extract-method
    #     """
    #     Process the context of a specified `Symbol`.

    #     This works by first processing the main printout for the symbol, which includes the symbol's
    #     documentation, docstring, and methods. Then, if the symbol is the main symbol, we process
    #     the context for the symbol's related symbols and dependencies.

    #     """
    #     with self.increased_indentation():
    #         self.process_headline(symbol)
    #         self.process_ast(symbol)

    #         if self._is_main_symbol():
    #             related_symbols_processed = 0
    #             self.process_message(f"Building context for related symbols -\n")

    #             for related_symbol in related_symbols:
    #                 if related_symbols_processed >= self.config.max_related_symbols_to_process:
    #                     break

    #                 # Check that the related symbol passes filter requirements
    #                 if not PyContextRetriever._pass_symbol_filter(symbol, related_symbol):
    #                     continue

    #                 if not self._below_context_limit():
    #                     break

    #                 if related_symbol not in self.obs_symbols:
    #                     self.process_symbol(related_symbol)
    #                     related_symbols_processed += 1

    #             # dependencies_processed = 0
    #             self.process_message(f"Building context for dependencies -\n")
    #             # all_dependencies = list(self.graph.get_symbol_dependencies(symbol))
    #             # filtered_dependencies = get_rankable_symbols(all_dependencies)

    #             # for dependency in filtered_dependencies:
    #             #     if dependencies_processed >= self.config.max_dependencies_to_process:
    #             #         break

    #             #     # Check that the dependency passes filter requirements
    #             #     if not PyContextRetriever._pass_symbol_filter(symbol, dependency):
    #             #         continue

    #             #     if not self._below_context_limit():
    #             #         break

    #             #     if dependency not in self.obs_symbols:
    #             #         try:
    #             #             self.process_symbol(dependency)
    #             #         except Exception as e:
    #             #             logger.error(f"Failure processing dependent {dependency} with {e}")
    #             #             continue
    #             #         dependencies_processed += 1

    #     self.obs_symbols.add(symbol)

    # def process_headline(self, symbol: Symbol) -> None:
    #     # Print the headline
    #     if self._is_main_symbol():
    #         self.process_message(f"Building context for primary symbol - {symbol.dotpath} -\n")
    #     else:
    #         self.process_message(f"{symbol.dotpath}\n")

    # def process_ast(self, symbol: Symbol) -> None:
    #     """Process the entire context for an AST object."""
    #     from automata.symbol import convert_to_ast_object

    #     ast_object = convert_to_ast_object(symbol)
    #     is_main_symbol = self._is_main_symbol()
    #     methods = sorted(PyContextRetriever._get_all_methods(ast_object), key=lambda x: x.name)

    #     with self.increased_indentation():
    #         if "test" in symbol.dotpath or "Config" in symbol.dotpath:
    #             with self.increased_indentation():
    #                 self.process_message(f"{py_ast_unparse(ast_object)}\n")
    #         else:
    #             if is_main_symbol:
    #                 self.process_imports(symbol)
    #             self.process_documentation(symbol, is_main_symbol)

    #             self.process_docstring(ast_object)

    #             if len(methods) > 0:
    #                 self.process_message("Methods:")
    #             for method in methods:
    #                 self.process_method(method, is_main_symbol)

    # def process_imports(self, symbol: Symbol) -> None:
    #     """Appends the import statements for a symbol to the context buffer."""
    #     # Compute the file path from the symbol's path
    #     file_path = os.path.join(
    #         get_root_py_fpath(), "..", str(symbol.dotpath).replace(".", os.path.sep)
    #     )
    #     while not os.path.isdir(os.path.dirname(file_path)):
    #         file_path = os.path.dirname(file_path)

    #     # Load the source code with AST
    #     with open(f"{file_path}.py", "r") as f:
    #         ast = py_ast_parse(f.read())

    #     # Find and print import statements
    #     imports = PyContextRetriever._get_all_imports(ast)
    #     if len(imports) > 0:
    #         self.process_message("Import Statements:")
    #         with self.increased_indentation():
    #             for import_node in imports:
    #                 self.process_message(py_ast_unparse(import_node))
    #             self.process_message("")  # Add an empty line for separation

    # def process_docstring(self, ast_object: AST) -> None:
    #     docstring = PyContextRetriever._get_docstring(ast_object)

    #     if docstring:
    #         self.process_message("Class Docstring:")
    #         with self.increased_indentation():
    #             self.process_message(docstring)
    #             self.process_message("")  # Add an empty line for separation

    # def process_documentation(self, symbol: Symbol, is_main_symbol: bool) -> None:
    #     """
    #     Process the documentation of a symbol, providing a summary or the entire source code
    #     depending on whether the symbol is the main symbol or not.
    #     """

    #     if self.doc_embedding_db is not None and self.doc_embedding_db.contains(symbol.dotpath):
    #         if is_main_symbol:
    #             document = self.doc_embedding_db.get(symbol.dotpath).document
    #         else:
    #             document = self.doc_embedding_db.get(symbol.dotpath).summary
    #         self.process_message("Class Document:")
    #         with self.increased_indentation():
    #             self.process_message(document)
    #             self.process_message("")  # Add an empty line for separation

    # def process_method(
    #     self, method: Union[AsyncFunctionDef, FunctionDef], is_main_symbol: bool
    # ) -> None:
    #     """
    #     Processes a specified method by printing its name, arguments, and return type.
    #     If we are processing the main symbol, we also print the method's code.
    #     """
    #     if PyContextRetriever._is_private_method(method):
    #         return
    #     with self.increased_indentation():
    #         if not is_main_symbol and method.name == "__init__" or is_main_symbol:
    #             for code_line in py_ast_unparse(method).split("\n"):
    #                 self.process_message(code_line)
    #         else:
    #             method_definition = (
    #                 f"{method.name}({PyContextRetriever._get_method_arguments(method)})"
    #             )
    #             return_annotation = PyContextRetriever._get_method_return_annotation(method)
    #             self.process_message(f"{method_definition} -> {return_annotation}\n")

    # def _is_main_symbol(self) -> bool:
    #     return self.indent_level == 1

    # def _below_context_limit(self) -> bool:
    #     return len(self.encoding_provider.encode(self.context)) < self.config.max_context

    # @staticmethod
    # def _get_all_imports(ast: AST):
    #     imports: List[Union[Import, ImportFrom]] = []
    #     for node in py_ast_walk(ast):
    #         if isinstance(node, Import):
    #             imports.append(node)
    #         elif isinstance(node, ImportFrom):
    #             imports.append(node)
    #     return imports

    # @staticmethod
    # def _pass_symbol_filter(primary_symbol: Symbol, secondary_symbol: Symbol) -> bool:
    #     primary_symbol_dotpath = primary_symbol.dotpath
    #     primary_package = primary_symbol_dotpath.split(".")[0]

    #     secondary_symbol_dotpath = secondary_symbol.dotpath
    #     secondary_package = secondary_symbol_dotpath.split(".")[0]
    #     return not (
    #         primary_symbol_dotpath in secondary_symbol_dotpath
    #         or primary_package != secondary_package
    #     )
