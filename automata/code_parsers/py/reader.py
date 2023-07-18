from __future__ import annotations

import copy
import logging
from ast import (
    AST,
    AsyncFunctionDef,
    ClassDef,
    FunctionDef,
    Module,
    fix_missing_locations,
    get_docstring,
)
from ast import unparse as pyast_unparse
from typing import Optional

from automata.core import find_syntax_tree_node, get_node_without_docstrings
from automata.singletons.py_module_loader import py_module_loader

logger = logging.getLogger(__name__)


class PyReader:
    """Code retriever for fetching python code"""

    NO_RESULT_FOUND_STR = "No Result Found."

    def __init__(self) -> None:
        pass

    def get_source_code(
        self, module_dotpath: str, object_path: Optional[str] = None
    ) -> str:
        """
        Gets code for a specified module, class, or function/method

        Args:
            module_dotpath (str): The path of the module in dot-separated format (e.g. 'package.module')
            object_path (Optional[str]): The path of the class, function, or method in dot-separated format
                (e.g. 'ClassName.method_name'). If None, the entire module code will be returned

        Returns:
            str: The code for the specified module, class, or function/method, or "No Result Found."
                if not found
        """
        if module := py_module_loader.fetch_ast_module(module_dotpath):
            if result := find_syntax_tree_node(module, object_path):
                return pyast_unparse(result)

        return PyReader.NO_RESULT_FOUND_STR

    def get_docstring(
        self, module_dotpath: str, object_path: Optional[str]
    ) -> str:
        """
        Gets the docstring for a specified module, class, or function/method

        Args:
            module_dotpath (str): The path of the module in dot-separated format (e.g. 'package.module')
            object_path (Optional[str]): The path of the class, function, or method in dot-separated format
                (e.g. 'ClassName.method_name'). If None, the module-level docstring will be returned

        Returns:
            str: The docstring for the specified module, class, or function/method, or "No Result Found."
                if not found
        """
        if module := py_module_loader.fetch_ast_module(module_dotpath):
            obj = find_syntax_tree_node(module, object_path)
            if isinstance(
                obj, (AsyncFunctionDef, FunctionDef, ClassDef, Module)
            ):
                return get_docstring(obj) or PyReader.NO_RESULT_FOUND_STR
        return PyReader.NO_RESULT_FOUND_STR

    def get_source_code_without_docstrings(
        self, module_dotpath: str, object_path: Optional[str]
    ) -> str:
        """
        Gets code for a specified module, class, or function/method

        Args:
            module_dotpath (str): The path of the module in dot-separated format (e.g. 'package.module')
            object_path (Optional[str]): The path of the class, function, or method in dot-separated format
                (e.g. 'ClassName.method_name'). If None, the entire module code will be returned

        Returns:
            str: The code for the specified module, class, or function/method, or "No Result Found."
                if not found
        """

        if module := py_module_loader.fetch_ast_module(module_dotpath):
            module_copy = copy.deepcopy(module)
            if result := find_syntax_tree_node(module_copy, object_path):
                result = get_node_without_docstrings(result)
                fix_missing_locations(result)
                return pyast_unparse(result)

        return PyReader.NO_RESULT_FOUND_STR

    @staticmethod
    def get_docstring_from_node(node: Optional[AST]) -> str:
        """
        Gets the docstring from the specified node

        Args:
            node: The FST node to get the docstring from
        """
        if not node:
            return PyReader.NO_RESULT_FOUND_STR

        if isinstance(node, (FunctionDef, ClassDef, AsyncFunctionDef, Module)):
            if doc_string := get_docstring(node):
                doc_string.replace('"""', "").replace("'''", "")
            else:
                return PyReader.NO_RESULT_FOUND_STR
        return ""
