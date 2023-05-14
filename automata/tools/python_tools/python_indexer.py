"""
This module provides a Python Abstract Syntax Tree (AST) indexer to help retrieve code and docstrings from
Python source code files in a specified directory. The PythonIndexer class supports retrieval of code
and docstrings for top-level functions, methods, and classes.

Dependencies:
    - ast
    - copy
    - logging
    - os
    - typing (Dict, Optional, Union, cast)
    - automata.core.utils

Classes:
    PythonIndexer: Main class to index and retrieve code and docstrings from Python source files.

Example:
    indexer = PythonIndexer(root_py_path())
    code = indexer.retrieve_code("module.path", "ClassName.method_name")
    docstring = indexer.retrieve_docstring("module.path", "ClassName.method_name")
"""
from __future__ import annotations

import ast
import logging
import os
import re
from _ast import AsyncFunctionDef, ClassDef, FunctionDef
from functools import cached_property
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

from automata.core.utils import root_path

logger = logging.getLogger(__name__)


class PythonIndexer:
    """
    A class to index Python source code files in a specified directory and retrieve code and docstrings.
    Attributes:
        abs_path (str): The absolute path to the root directory containing Python source code files to be indexed.
        module_dict (Dict[str, Module]): A dictionary with module paths as keys and AST Module objects as values.

    Methods:
        __init__(self, rel_path: str) -> None
        retrieve_code(self, module_path: str, object_path: Optional[str]) -> Optional[str]
        retrieve_docstring(self, module_path: str, object_path: Optional[str]) -> Optional[str]
    """

    NO_RESULT_FOUND_STR = "No Result Found."
    PATH_SEP = "."

    def __init__(self, rel_path: str) -> None:
        """
        Initializes the PythonIndexer with the specified root directory and builds the module dictionary.

        Args:
            rel_path (str): The root directory containing Python source code files to be indexed.
        """

        self.abs_path = os.path.join(root_path(), rel_path)

    @cached_property
    def module_dict(self) -> Dict[str, RedBaron]:
        # TODO: cache by module
        return self._build_module_dict()

    def retrieve_code_without_docstrings(
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

        if module_path not in self.module_dict:
            return PythonIndexer.NO_RESULT_FOUND_STR

        module = RedBaron(
            self.module_dict[module_path].dumps()
        )  # create a copy because we'll remove docstrings
        result = self.find_module_class_function_or_method(module, object_path)

        if result:
            PythonIndexer._remove_docstrings(result)
            return result.dumps()
        else:
            return PythonIndexer.NO_RESULT_FOUND_STR

    def retrieve_code(self, module_path: str, object_path: Optional[str] = None) -> str:
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

        if module_path not in self.module_dict:
            return PythonIndexer.NO_RESULT_FOUND_STR

        module = self.module_dict[module_path]
        result = self.find_module_class_function_or_method(module, object_path)

        if result:
            return result.dumps()
        else:
            return PythonIndexer.NO_RESULT_FOUND_STR

    def find_expression_context(
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
        for module_path, module in self.module_dict.items():
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

    def retrieve_parent_function_name_by_line(self, module_path: str, line_number: int) -> str:
        """
        Retrieve code for a specified module, class, or function/method.

        Args:
            module_path (str): The path of the module in dot-separated format (e.g. 'package.module').
            line_number (int): The line number of the code to retrieve.

        Returns:
            str: The code for the specified module, class, or function/method, or "No Result Found."
                if not found.
        """

        if module_path not in self.module_dict:
            return PythonIndexer.NO_RESULT_FOUND_STR

        node = self.module_dict[module_path].at(line_number)
        if node.type != "def":
            node = node.parent_find("def")
        if node:
            if node.parent[0].type == "class":
                return f"{node.parent.name}.{node.name}"
            else:
                return node.name
        else:
            return PythonIndexer.NO_RESULT_FOUND_STR

    def retrieve_parent_function_num_code_lines(
        self, module_path: str, line_number: int
    ) -> Union[int, str]:
        if module_path not in self.module_dict:
            return PythonIndexer.NO_RESULT_FOUND_STR

        node = self.module_dict[module_path].at(line_number)
        if node.type != "def":
            node = node.parent_find("def")
        if not node:
            return PythonIndexer.NO_RESULT_FOUND_STR
        return (
            node.absolute_bounding_box.bottom_right.line
            - node.absolute_bounding_box.top_left.line
            + 1
        )

    def retrieve_parent_code_by_line(
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

        if module_path not in self.module_dict:
            return PythonIndexer.NO_RESULT_FOUND_STR
        module = self.module_dict[module_path]
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
                        docstring = PythonIndexer._get_docstring(pointer[x])
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

    def _create_line_number_tuples(self, node, start_line, start_col):
        result = []
        for i, line in enumerate(node.dumps().strip().splitlines()):
            if i == 0 and not line.startswith(" " * (start_col - 1)):
                line = " " * (start_col - 1) + line
            result.append((start_line + i, line))
        return result

    def retrieve_docstring(self, module_path: str, object_path: Optional[str]) -> str:
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

        if module_path not in self.module_dict:
            return PythonIndexer.NO_RESULT_FOUND_STR

        module = self.module_dict[module_path]
        result = self.find_module_class_function_or_method(module, object_path)

        if result:
            return PythonIndexer._get_docstring(result) or PythonIndexer.NO_RESULT_FOUND_STR
        else:
            return PythonIndexer.NO_RESULT_FOUND_STR

    @staticmethod
    def _get_docstring(node) -> str:
        if isinstance(node, (ClassNode, DefNode, RedBaron)):
            filtered_nodes = node.filtered()  # get rid of extra whitespace
            if isinstance(filtered_nodes[0], StringNode):
                return filtered_nodes[0].value.replace('"""', "").replace("'''", "")
        return ""

    def _build_module_dict(self) -> Dict[str, RedBaron]:
        """
        Builds the module dictionary by walking through the root directory and creating FST Module objects
        for each Python source file. The module paths are used as keys in the dictionary.

        Returns:
            Dict[str, RedBaron]: A dictionary with module paths as keys and RedBaron objects as values.
        """

        module_dict = {}

        for root, _, files in os.walk(self.abs_path):
            for file in files:
                if file.endswith(".py"):
                    module_path = os.path.join(root, file)
                    module = self._load_module_from_path(module_path)
                    if module:
                        module_rel_path = PythonIndexer._relative_module_path(
                            self.abs_path, module_path
                        )
                        module_dict[module_rel_path] = module
        return module_dict

    @staticmethod
    def _relative_module_path(root_abs_path, module_path):
        module_rel_path = (os.path.relpath(module_path, root_abs_path).replace(os.path.sep, "."))[
            :-3
        ]
        return module_rel_path

    def get_module_path(self, module_obj: RedBaron) -> str:
        """
        Returns the module path for the specified module object.

        Args:
            module_obj (Module): The module object.

        Returns:
            str: The module path for the specified module object.
        """

        for module_path, module in self.module_dict.items():
            if module is module_obj:
                return module_path
        return PythonIndexer.NO_RESULT_FOUND_STR

    @staticmethod
    def build_overview(path) -> str:
        """
        Loops over the directory python files and returns a string that provides an overview of the PythonParser's state.
        Returns:
            str: A string that provides an overview of the PythonParser's state.
        **NOTE: This method uses AST, not RedBaron, because RedBaron initialization is slow and unnecessary for this method.
        """
        result_lines = []

        for root, _, files in os.walk(path):
            for file in files:
                if file.endswith(".py"):
                    module_path = os.path.join(root, file)
                    module = ast.parse(open(module_path).read())
                    relative_module_path = PythonIndexer._relative_module_path(path, module_path)
                    result_lines.append(relative_module_path)
                    PythonIndexer._overview_traverse_helper(module, result_lines)
        return "\n".join(result_lines)

    @staticmethod
    def _overview_traverse_helper(node, line_items, num_spaces=1):
        if isinstance(node, ClassDef):
            line_items.append("  " * num_spaces + " - cls " + node.name)
        elif isinstance(node, FunctionDef) or isinstance(node, AsyncFunctionDef):
            line_items.append("  " * num_spaces + " - func " + node.name)

        for child in ast.iter_child_nodes(node):
            PythonIndexer._overview_traverse_helper(child, line_items, num_spaces + 1)

    @staticmethod
    def _load_module_from_path(path) -> Optional[RedBaron]:
        """
        Loads and returns an FST object for the given file path.

        Args:
            path (str): The file path of the Python source code.

        Returns:
            Module: RedBaron FST object.
        """

        try:
            module = RedBaron(open(path).read())
            return module
        except Exception as e:
            logger.error(f"Failed to load module '{path}' due to: {e}")
            return None

    @staticmethod
    def find_module_class_function_or_method(
        code_obj: Union[RedBaron, ClassNode], object_path: Optional[str]
    ) -> Optional[Union[Node, RedBaron]]:
        """
        Find a module, or find a function, method, or class inside a module.

        Args:
            code_obj (RedBaron): The  red baron FST object.
            object_path (Optional[str]): The dot-separated object path (e.g., 'ClassName.method_name'). If None,
                the module is returned.

        Returns:
            Optional[Union[Def, Class, Module]]: The found def, or class node, or None if not found.
        """

        if not object_path:
            return code_obj

        obj_parts = object_path.split(PythonIndexer.PATH_SEP)

        node = code_obj
        while node and obj_parts:
            obj_name = obj_parts.pop(0)
            node = PythonIndexer._find_node(node, obj_name)
        return node

    @staticmethod
    def _find_node(code_obj: RedBaron, obj_name: str) -> Optional[Union[DefNode, ClassNode]]:
        """
        Find a DefNode or ClassNode node with the specified name within the given
        FST code object.

        Args:
            code_obj (RedBaron): The FST code object (RedBaron or Node) to search.
            obj_name (str): The name of the object to find.

        Returns:
            Optional[Union[DefNode, ClassNode]]: The found node, or None.
        """
        return code_obj.find(lambda identifier: identifier in ("def", "class"), name=obj_name)

    @staticmethod
    def find_imports(module: RedBaron) -> Optional[NodeList]:
        """
        Find all imports in a module.

        Args:
            module (RedBaron): The module to search.

        Returns:
            Optional[NodeList]: A list of ImportNode and FromImportNode objects.
        """
        return module.find_all(lambda identifier: identifier in ("import", "from_import"))

    @staticmethod
    def find_import_by_name(
        module: RedBaron, import_name: str
    ) -> Optional[Union[ImportNode, FromImportNode]]:
        """
        Find an import by name.

        Args:
            module (RedBaron): The module to search.
            import_name (str): The name of the import to find.

        Returns:
            Optional[Union[ImportNode, FromImportNode]]: The found import, or None if not found.
        """
        return module.find(
            lambda identifier: identifier in ("import", "from_import"), name=import_name
        )

    @staticmethod
    def find_all_functions_and_classes(module: RedBaron) -> NodeList:
        """
        Find all imports in a module.

        Args:
            module (RedBaron): The module to search.

        Returns:
            NodeList: A list of ClassNode and DefNode objects.
        """
        return module.find_all(lambda identifier: identifier in ("class", "def"))

    @staticmethod
    def _remove_docstrings(node: Union[Node, RedBaron]) -> None:
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
                    PythonIndexer._remove_docstrings(child_node)

    # def _filter_code_lines(self, node: Union[Node, RedBaron]) -> List[str]:
    #     """
    #     Returns lines of code that are not empty or comments or docstrings.
    #
    #     Args:
    #         node: The FST node to filter.
    #     """
    #     body = node.value.copy()
    #     body = body.filter(lambda x: x.type != "string" or not x.value.startswith('"""'))
    #     source_code_lines = body.dumps().splitlines()
    #     predicate = (
    #         lambda line: not line.strip().startswith("#")
    #         and not line.strip().startswith("@")
    #         and not line.strip() == ""
    #     )
    #     source_code_lines = [line for line in source_code_lines if predicate(line)]
    #     return source_code_lines
