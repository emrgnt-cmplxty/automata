import os
from contextlib import contextmanager
from typing import List, Optional, Set

from redbaron import RedBaron

from automata_docs.core.indexing.python_indexing.python_code_retriever import PythonCodeRetriever
from automata_docs.core.indexing.python_indexing.syntax_tree_navigation import (
    find_method_call_by_location,
)
from automata_docs.core.indexing.utils import build_repository_overview
from automata_docs.core.search.symbol_graph import SymbolGraph
from automata_docs.core.search.symbol_utils import convert_to_fst_object, get_rankable_symbols
from automata_docs.core.symbol.symbol_types import Descriptor, Symbol, SymbolReference
from automata_docs.core.utils import root_py_path


class PythonContextRetrieverConfig:
    def __init__(
        self,
        spacer: str = "  ",
        max_dependency_print_depth: int = 2,
        max_recursion_depth: int = 1,
        nearest_symbols_count: int = 10,
        print_imports=False,
        process_directory_structure=False,
        process_docstrings=True,
        process_variables=True,
        process_methods=True,
        process_methods_constructor=True,
        process_methods_summary=False,
        process_nearest_symbols=True,
        process_dependencies=False,
        process_references=False,
        process_callers=False,
    ):
        self.spacer = spacer
        self.nearest_symbols_count = nearest_symbols_count
        self.max_dependency_print_depth = max_dependency_print_depth
        self.max_recursion_depth = max_recursion_depth
        self.print_imports = print_imports
        self.process_directory_structure = process_directory_structure
        self.process_docstrings = process_docstrings
        self.process_variables = process_variables
        self.process_methods = process_methods
        self.process_methods_constructor = process_methods_constructor
        self.process_methods_summary = process_methods_summary
        self.process_nearest_symbols = process_nearest_symbols
        self.process_dependencies = process_dependencies
        self.process_references = process_references
        self.process_callers = process_callers


class PythonContextRetriever:
    def __init__(
        self,
        graph: SymbolGraph,
        config: PythonContextRetrieverConfig = PythonContextRetrieverConfig(),
    ):
        self.graph = graph
        self.config = config
        self.indent_level = 0
        self.reset()

    @contextmanager
    def IndentManager(self):
        self.indent_level += 1
        yield
        self.indent_level -= 1

    def process_message(self, message: str):
        def indent() -> str:
            return self.config.spacer * self.indent_level

        self.message += "\n".join([f"{indent()}{ele}" for ele in message.split("\n")]) + "\n"

    def reset(self) -> None:
        self.message = ""
        self.obs_symbols: Set[Symbol] = set([])
        self.global_level = 0

    def process_symbol(
        self,
        symbol: Symbol,
        ranked_symbols: List[Symbol] = [],
    ) -> None:
        # Check if the symbol has already been processed
        if symbol in self.obs_symbols:
            return
        self.obs_symbols.add(symbol)

        if self._is_first_symbol_call() and self.config.process_directory_structure:
            self.process_directory_structure(symbol)

        self.process_headline(symbol)
        if self.indent_level <= self.config.max_dependency_print_depth:
            with self.IndentManager():
                self.process_class(symbol)
                if self.indent_level <= self.config.max_recursion_depth:
                    if self.config.process_nearest_symbols:
                        self.process_nearest_symbols(ranked_symbols)
                    if self.config.process_dependencies:
                        self.process_dependencies(symbol)
                    if self.config.process_references:
                        self.process_references(symbol)
                    if self.config.process_callers:
                        self.process_callers(symbol)

    def process_directory_structure(self, symbol: Symbol) -> None:
        # Print the directory structure
        self.process_message(f"Local Directory Structure:")
        with self.IndentManager():
            symbol_path = str(symbol.path).replace(".", os.path.sep)
            dir_path = os.path.join(root_py_path(), "..", symbol_path)
            while not os.path.isdir(dir_path):
                dir_path = os.path.dirname(dir_path)
            overview = build_repository_overview(dir_path, skip_func=True)
            self.process_message(f"{overview}\n")

    def process_headline(self, symbol: Symbol) -> None:
        # Print the headline
        if self._is_first_symbol_call():
            self.process_message(f"Context for -\n{symbol.path} -\n")
        else:
            self.process_message(f"{symbol.path}\n")

    def process_class(self, symbol: Symbol) -> None:
        def process_imports(symbol: Symbol) -> None:
            # Compute the file path from the symbol's path
            file_path = os.path.join(
                root_py_path(), "..", str(symbol.path).replace(".", os.path.sep)
            )
            while not os.path.isdir(os.path.dirname(file_path)):
                file_path = os.path.dirname(file_path)

            # Load the source code with RedBaron
            with open(file_path + ".py", "r") as f:
                red = RedBaron(f.read())

            # Find and print import statements
            self.process_message("Import Statements:")
            with self.IndentManager():
                imports = red.find_all("ImportNode")
                from_imports = red.find_all("FromImportNode")
                for import_node in imports + from_imports:
                    self.process_message(str(import_node.dumps()))
                self.process_message("")  # Add an empty line for separation

        def process_docstring(ast_object: RedBaron) -> None:
            docstring = PythonContextRetriever._get_docstring(ast_object)
            # Print the docstring if it exists
            if docstring:
                self.process_message("Class Docstring:")
                with self.IndentManager():
                    self.process_message(docstring)
                    self.process_message("")  # Add an empty line for separation

        def process_variables(ast_object: RedBaron) -> None:
            assignments = ast_object.find_all("assignment")
            num_good_assignments = len(
                [
                    assignment.parent == ast_object or "self." in str(assignment.target.dumps())
                    for assignment in assignments
                ]
            )
            if num_good_assignments > 0:
                self.process_message(f"Variables:")

            with self.IndentManager():
                for assignment in assignments:
                    if assignment.parent == ast_object or "self." in str(
                        assignment.target.dumps()
                    ):
                        self.process_message(
                            f"{str(assignment.target.dumps())}={str(assignment.value.dumps())}"
                        )
                self.process_message("")

        def process_methods(ast_object: RedBaron) -> None:
            methods = sorted(ast_object.find_all("DefNode"), key=lambda x: x.name)
            if len(methods) > 0:
                self.process_message(f"Methods:")
            with self.IndentManager():
                for method in methods:
                    self.process_method(method)

        # Convert the symbol to an AST object, return if it fails
        try:
            ast_object = convert_to_fst_object(symbol)
        except Exception as e:
            print(f"Error {e} while converting symbol {symbol.descriptors[-1].name}.")
            return None

        # If this is the first symbol call, we optionally print import statements
        if self._is_first_symbol_call():
            if self.config.print_imports:
                process_imports(symbol)

        # Check config for which parts of the class to print
        if self.config.process_docstrings:
            process_docstring(ast_object)
        if self.config.process_variables:
            process_variables(ast_object)
        if self.config.process_methods:
            process_methods(ast_object)

    def process_method(self, method: RedBaron, detailed: bool = False) -> None:
        if PythonContextRetriever._is_private_method(method):
            return
        if self._is_first_symbol_call():  # e.g. top level
            for code_line in method.dumps().split("\n"):
                self.process_message(code_line)
        else:
            valid_method_filters = ["init"]
            if self.config.process_methods_constructor:
                # Process the method constructor
                if self.config.process_methods_constructor:
                    if self._is_within_second_call():  # e.g. a dependency or related symbol
                        is_valid_method = False
                        for filter_ in valid_method_filters:
                            if filter_ in method.name:
                                is_valid_method = True
                        if is_valid_method:
                            for code_line in method.dumps().split("\n"):
                                self.process_message(code_line)
            # Process the method signature and return annotation
            if self.config.process_methods_summary:
                method_definition = f"{method.name}({method.arguments.dumps()})"
                return_annotation = (
                    method.return_annotation.dumps() if method.return_annotation else "None"
                )
                self.process_message(f"{method_definition} -> {return_annotation}\n")

    def process_dependencies(self, symbol: Symbol) -> None:
        if self._is_first_symbol_call():
            self.process_message("Dependencies:")
            with self.IndentManager():
                all_dependencies = list(self.graph.get_symbol_dependencies(symbol))
                filtered_dependencies = get_rankable_symbols(all_dependencies)
                for dependency in filtered_dependencies:
                    if not PythonContextRetriever._is_class(dependency):
                        continue
                    if dependency == symbol:
                        continue
                    if (
                        "automata" not in dependency.uri
                    ):  # TODO - Make this cleaner in case "automata" is not the key URI
                        continue
                    self.process_symbol(dependency)

    def process_references(self, symbol: Symbol) -> None:
        references = self.graph.get_references_to_symbol(symbol)
        if len(references) > 0:
            self.process_message("References:")
            with self.IndentManager():
                for file_path, symbol_references in references.items():
                    self.process_message(f"File: {file_path}")
                    with self.IndentManager():
                        for ref in symbol_references:
                            self.process_message(
                                f"Line: {ref.line_number}, Column: {ref.column_number}"
                            )

    def process_callers(self, symbol: Symbol) -> None:
        if self.indent_level < 2:
            self.process_message(f"Callers:")
        else:
            self.process_message(f"Caller Callers:")

        with self.IndentManager():
            all_potential_callers = list(self.graph.get_potential_symbol_callers(symbol))

            def find_call(caller: SymbolReference) -> Optional[RedBaron]:
                module = convert_to_fst_object(caller.symbol)
                line_number = caller.line_number
                column_number = caller.column_number + len(symbol.descriptors[-1].name)
                return find_method_call_by_location(module, line_number, column_number)

            for caller in all_potential_callers:
                if "test" in str(caller.symbol.path):
                    continue

                call = find_call(caller)
                if call is None:
                    continue

                self.process_message(str(caller.symbol.path))

                # Call a level deeper when we encounter a factory or builder
                if "Factory" in str(caller.symbol.path) or "Builder" in str(caller.symbol.path):
                    self.process_callers(caller.symbol)

                with self.IndentManager():
                    call_parent = call.parent if call is None else None  # type: ignore
                    if call_parent is None:
                        continue
                    self.process_message(str(call_parent.dumps()))

    def process_nearest_symbols(
        self,
        search_list: List[Symbol],
    ) -> None:
        self.process_message("Closely Related Symbols:")

        def bespoke_test_handler(test_symbol) -> bool:
            try:
                ast_object = convert_to_fst_object(test_symbol)
            except Exception as e:
                print(f"Error {e} while converting symbol {test_symbol.descriptors[-1].name}.")
                return False
            with self.IndentManager():
                self.process_headline(test_symbol)
                with self.IndentManager():
                    self.process_message(ast_object.dumps())
            return True

        with self.IndentManager():
            if len(search_list) > 0:
                printed_nearby_symbols = 0
                for ranked_symbol in search_list:
                    if printed_nearby_symbols >= self.config.nearest_symbols_count:
                        break
                    # Bespoke handling for test class
                    if "test" in str(ranked_symbol.path):
                        result = bespoke_test_handler(ranked_symbol)
                        if result:
                            printed_nearby_symbols += 1
                        else:
                            continue

                    if ranked_symbol.symbol_kind_by_suffix() != Descriptor.PythonKinds.Class:
                        continue
                    elif ranked_symbol in self.obs_symbols:
                        continue
                    else:
                        printed_nearby_symbols += 1
                        self.process_symbol(ranked_symbol)

    def _is_first_symbol_call(self) -> bool:
        return self.indent_level <= 2

    def _is_within_second_call(self) -> bool:
        return self.indent_level <= 4

    @staticmethod
    def _is_private_method(ast_object):
        return ast_object.name[0] == "_" and ast_object.name[1] != "_"

    @staticmethod
    def _is_class(symbol):
        return symbol.symbol_kind_by_suffix() == Descriptor.PythonKinds.Class

    @staticmethod
    def _get_docstring(ast_object):
        raw_doctring = PythonCodeRetriever.get_docstring_from_node(ast_object).split("\n")
        return "\n".join([ele.strip() for ele in raw_doctring]).strip()
