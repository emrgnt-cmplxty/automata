from __future__ import annotations

import ast
import logging
import os
import re
from _ast import AsyncFunctionDef, ClassDef, FunctionDef
from functools import cached_property, lru_cache
from typing import Dict, Optional, Union

from redbaron import (
    ClassNode,
    DefNode,
    FromImportNode,
    ImportNode,
    Node,
    NodeList,
    RedBaron,
    StringNode,
)

from automata.core.code_indexing.python_ast_indexer import PythonASTIndexer
from automata.core.code_indexing.python_ast_navigator import PythonASTNavigator
from automata.core.utils import root_path, root_py_path

logger = logging.getLogger(__name__)
FSTNode = Union[Node, RedBaron]


class PythonCodeInspector:
    def __init__(self, python_indexer: PythonASTIndexer) -> None:
        self.indexer = python_indexer

    def get_source_code(self, module_path: str, object_path: Optional[str] = None) -> str:
        """
        Gets code for a specified module, class, or function/method.

        Args:
            module_path (str): The path of the module in dot-separated format (e.g. 'package.module').
            object_path (Optional[str]): The path of the class, function, or method in dot-separated format
                (e.g. 'ClassName.method_name'). If None, the entire module code will be returned.

        Returns:
            str: The code for the specified module, class, or function/method, or "No Result Found."
                if not found.
        """

        module = self.indexer.find_module_object(module_path)
        result = PythonASTNavigator.find_node(module, object_path)
        return result.dumps() if result else PythonASTIndexer.NO_RESULT_FOUND_STR

    def get_docstring(self, module_path: str, object_path: Optional[str]) -> str:
        """
        Retrieve the docstring for a specified module, class, or function/method.

        Args:
            module_path (str): The path of the module in dot-separated format (e.g. 'package.module').
            object_path (Optional[str]): The path of the class, function, or method in dot-separated format
                (e.g. 'ClassName.method_name'). If None, the module-level docstring will be returned.

        Returns:
            str: The docstring for the specified module, class, or function/method, or "No Result Found."
                if not found.
        """

        module = self.indexer.find_module_object(module_path)
        return PythonCodeInspector._get_docstring(PythonASTNavigator.find_node(module, object_path))

    def get_source_code_without_docstrings(
        self, module_path: str, object_path: Optional[str]
    ) -> str:
        """
        Retrieve code for a specified module, class, or function/method.

        Args:
            module_path (str): The path of the module in dot-separated format (e.g. 'package.module').
            object_path (Optional[str]): The path of the class, function, or method in dot-separated format
                (e.g. 'ClassName.method_name'). If None, the entire module code will be returned.

        Returns:
            str: The code for the specified module, class, or function/method, or "No Result Found."
                if not found.
        """

        def _remove_docstrings(node: FSTNode) -> None:
            """
            Remove docstrings from the specified node, recursively.

            Args:
                node: The FST node
                    to remove docstrings from.
            """

            if isinstance(node, (DefNode, ClassNode, RedBaron)):
                filtered_node = node.filtered()
                if isinstance(filtered_node[0], StringNode):
                    index = filtered_node[0].index_on_parent
                    node.pop(index)
                child_nodes = node.find_all(lambda identifier: identifier in ("def", "class"))
                for child_node in child_nodes:
                    if child_node is not node:
                        _remove_docstrings(child_node)

        module = self.indexer.find_module_object(module_path)

        module = (
            RedBaron(module.dumps()) if module else None
        )  # create a copy because we'll remove docstrings
        result = PythonASTNavigator.find_node(module, object_path)

        if result:
            _remove_docstrings(result)
            return result.dumps()
        else:
            return PythonASTIndexer.NO_RESULT_FOUND_STR

    def get_parent_function_name_by_line(self, module_path: str, line_number: int) -> str:
        """
        Retrieve code for a specified module, class, or function/method.

        Args:
            module_path (str): The path of the module in dot-separated format (e.g. 'package.module').
            line_number (int): The line number of the code to retrieve.

        Returns:
            str: The code for the specified module, class, or function/method, or "No Result Found."
                if not found.
        """

        module = self.indexer.find_module_object(module_path)
        if not module:
            return PythonASTIndexer.NO_RESULT_FOUND_STR

        node = module.at(line_number)
        if node.type != "def":
            node = node.parent_find("def")
        if node:
            if node.parent[0].type == "class":
                return f"{node.parent.name}.{node.name}"
            else:
                return node.name
        else:
            return PythonASTIndexer.NO_RESULT_FOUND_STR

    def get_parent_function_num_code_lines(
        self, module_path: str, line_number: int
    ) -> Union[int, str]:
        """
        Retrieve number of code lines for a specified module, class, or function/method.

        Args:
            module_path (str): The path of the module in dot-separated format (e.g. 'package.module').
            line_number (int): The line number of the code to retrieve around.

        Returns:
            int: The number of code lines for the specified module, class, or function/method, or "No Result Found."

        """
        module = self.indexer.find_module_object(module_path)
        if not module:
            return PythonASTIndexer.NO_RESULT_FOUND_STR

        node = module.at(line_number)
        if node.type != "def":
            node = node.parent_find("def")
        if not node:
            return PythonASTIndexer.NO_RESULT_FOUND_STR
        return (
            node.absolute_bounding_box.bottom_right.line
            - node.absolute_bounding_box.top_left.line
            + 1
        )

    def get_parent_code_by_line(
        self, module_path: str, line_number: int, return_numbered=False
    ) -> str:
        """
        Retrieve code for a specified module, class, or function/method.

        Args:
            module_path (str): The path of the module in dot-separated format (e.g. 'package.module').
            line_number (int): The line number of the code to retrieve.
            return_numbered (bool): Whether to return the code with line numbers prepended.

        Returns:
            str: The code for the specified module, class, or function/method, or "No Result Found."
                if not found.
        """

        module = self.indexer.find_module_object(module_path)
        if not module:
            return PythonASTIndexer.NO_RESULT_FOUND_STR
        node = module.at(line_number)

        # retarget def or class node
        if node.type not in ("def", "class") and node.parent_find(
            lambda identifier: identifier in ("def", "class")
        ):
            node = node.parent_find(lambda identifier: identifier in ("def", "class"))

        path = node.path().to_baron_path()
        pointer = module
        result = []

        for entry in path:
            if isinstance(entry, int):
                pointer = pointer.node_list
                for x in range(entry):
                    start_line, start_col = (
                        pointer[x].absolute_bounding_box.top_left.line,
                        pointer[x].absolute_bounding_box.top_left.column,
                    )

                    if pointer[x].type == "string" and pointer[x].value.startswith('"""'):
                        result += self._create_line_number_tuples(
                            pointer[x], start_line, start_col
                        )
                    if pointer[x].type in ("def", "class"):
                        docstring = PythonCodeInspector._get_docstring(pointer[x])
                        node_copy = pointer[x].copy()
                        node_copy.value = '"""' + docstring + '"""'
                        result += self._create_line_number_tuples(node_copy, start_line, start_col)
                pointer = pointer[entry]
            else:
                start_line, start_col = (
                    pointer.absolute_bounding_box.top_left.line,
                    pointer.absolute_bounding_box.top_left.column,
                )
                node_copy = pointer.copy()
                node_copy.value = ""
                result += self._create_line_number_tuples(node_copy, start_line, start_col)
                pointer = getattr(pointer, entry)

        start_line, start_col = (
            pointer.absolute_bounding_box.top_left.line,
            pointer.absolute_bounding_box.top_left.column,
        )
        result += self._create_line_number_tuples(pointer, start_line, start_col)

        prev_line = 1
        result_str = ""
        for t in result:
            if t[0] > prev_line + 1:
                result_str += "...\n"
            if return_numbered:
                result_str += f"{t[0]}: {t[1]}\n"
            else:
                result_str += f"{t[1]}\n"
            prev_line = t[0]
        return result_str

    def get_expression_context(
        self,
        expression: str,
        symmetric_width: int = 2,
    ) -> str:
        """
        Inspects the codebase for lines containing the expression and returns the line number and
        surrounding lines.

        Args:
            root_dir (str): The root directory to search.
            expression (str): The expression to search for.

        Returns:
            str: The context associated with the expression.
        """

        result = ""
        pattern = re.compile(expression)
        for module_path in self.indexer.get_all_module_paths():
            module = self.indexer.find_module_object(module_path)
            if not module:
                raise Exception(f"Could not find expected module {module_path}")
            lines = module.dumps().splitlines()
            for i, line in enumerate(lines):
                lineno = i + 1  # rebardon lines are 1 indexed, same as in an editor
                if pattern.search(line):
                    lower_index = max(i - symmetric_width, 0)
                    upper_index = min(i + symmetric_width, len(lines))

                    raw_code = "\n".join(lines[lower_index : upper_index + 1])
                    result += f"{module_path}"

                    node = module.at(lineno)
                    if node.type not in ("def", "class"):
                        node = node.parent_find(lambda identifier: identifier in ("def", "class"))

                    if node:
                        result += f".{node.name}"

                    linespan_str = (
                        f"L{lineno}"
                        if not symmetric_width
                        else f"L{lower_index + 1}-{upper_index + 1}"
                    )
                    result += f"\n{linespan_str}\n```{raw_code}```\n\n"

        return result

    @staticmethod
    def _create_line_number_tuples(node: FSTNode, start_line: int, start_col: int):
        result = []
        for i, line in enumerate(node.dumps().strip().splitlines()):
            if i == 0 and not line.startswith(" " * (start_col - 1)):
                line = " " * (start_col - 1) + line
            result.append((start_line + i, line))
        return result

    @staticmethod
    def _get_docstring(node: Optional[FSTNode]) -> str:
        if not node:
            return PythonASTIndexer.NO_RESULT_FOUND_STR

        if isinstance(node, (ClassNode, DefNode, RedBaron)):
            filtered_nodes = node.filtered()  # get rid of extra whitespace
            if isinstance(filtered_nodes[0], StringNode):
                return filtered_nodes[0].value.replace('"""', "").replace("'''", "")
        return ""