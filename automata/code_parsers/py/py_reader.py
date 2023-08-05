"""Defines the core logic for reading python files, e.g. `PyReader`"""
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
)
from ast import get_docstring as get_ast_docstring
from ast import unparse as pyast_unparse
from typing import Optional

from automata.core import find_syntax_tree_node, get_node_without_docstrings

logger = logging.getLogger(__name__)


class PyReader:
    """Code retriever for fetching python code"""

    NO_RESULT_FOUND_STR = "No Result Found."

    def __init__(self) -> None:
        pass

    def __eq__(self, other: object) -> bool:
        # Since there are no internal variables, just check if other is an
        # instance of PyReader
        return isinstance(other, PyReader)

    def get_source_code(
        self, module_dotpath: str, node_path: Optional[str] = None
    ) -> str:
        """Gets code for a specified module, class, or function/method"""
        from automata.singletons.py_module_loader import py_module_loader

        if module := py_module_loader.fetch_ast_module(module_dotpath):
            if result := find_syntax_tree_node(module, node_path):
                return pyast_unparse(result)

        return PyReader.NO_RESULT_FOUND_STR

    def get_docstring(
        self, module_dotpath: str, node_path: Optional[str]
    ) -> str:
        """Gets the docstring for a specified module, class, or function/method"""
        from automata.singletons.py_module_loader import py_module_loader

        if module := py_module_loader.fetch_ast_module(module_dotpath):
            if not node_path:
                return (
                    get_ast_docstring(module) or PyReader.NO_RESULT_FOUND_STR
                )
            obj = find_syntax_tree_node(module, node_path)
            if isinstance(
                obj, (AsyncFunctionDef, FunctionDef, ClassDef, Module)
            ):
                return get_ast_docstring(obj) or PyReader.NO_RESULT_FOUND_STR
        return PyReader.NO_RESULT_FOUND_STR

    def get_source_code_without_docstrings(
        self, module_dotpath: str, node_path: Optional[str]
    ) -> str:
        """Gets code for a specified module, class, or function/method"""
        from automata.singletons.py_module_loader import py_module_loader

        if module := py_module_loader.fetch_ast_module(module_dotpath):
            module_copy = copy.deepcopy(module)
            if result := find_syntax_tree_node(module_copy, node_path):
                result = get_node_without_docstrings(result)
                fix_missing_locations(result)
                return pyast_unparse(result)

        return PyReader.NO_RESULT_FOUND_STR

    @staticmethod
    def get_docstring_from_node(node: Optional[AST]) -> str:
        """Gets the docstring from the specified node"""

        if not node:
            return PyReader.NO_RESULT_FOUND_STR

        if isinstance(node, (FunctionDef, ClassDef, AsyncFunctionDef, Module)):
            if doc_string := get_ast_docstring(node):
                return doc_string.replace('"""', "").replace("'''", "")
            else:
                return PyReader.NO_RESULT_FOUND_STR
        return ""
