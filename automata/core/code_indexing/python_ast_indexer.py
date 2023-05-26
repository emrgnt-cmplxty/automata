from __future__ import annotations

import ast
import logging
import os
from _ast import AsyncFunctionDef, ClassDef, FunctionDef
from functools import cached_property, lru_cache
from typing import Dict, List, Optional

from redbaron import RedBaron

from automata.core.utils import root_path, root_py_path

logger = logging.getLogger(__name__)


class PythonASTIndexer:
    NO_RESULT_FOUND_STR = "No Result Found."
    PATH_SEP = "."

    def __init__(self, rel_path: str):
        self.abs_path = os.path.join(root_path(), rel_path)

    @cached_property
    def module_dict(self) -> Dict[str, RedBaron]:
        # TODO: cache by module
        return self._build_module_dict()

    @classmethod
    @lru_cache(maxsize=1)
    def cached_default(cls) -> "PythonASTIndexer":
        return cls(root_py_path())

    @staticmethod
    def build_repository_overview(path) -> str:
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
                    relative_module_path = PythonASTIndexer._relative_module_path(
                        path, module_path
                    )
                    result_lines.append(relative_module_path)
                    PythonASTIndexer._overview_traverse_helper(module, result_lines)
        return "\n".join(result_lines)

    def find_module_object(self, module_path: str) -> Optional[RedBaron]:
        """
        Find a module, or find a function, method, or class inside a module.

        Args:
            module_path (str): The dot-separated module path (e.g., 'module.submodule.subsubmodule').

        Returns:
            Optional[Union[Def, Class, Module]]: The found def, or class node, or None if not found.
        """

        module = self.module_dict.get(module_path)
        return module

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
        return PythonASTIndexer.NO_RESULT_FOUND_STR

    def get_all_module_paths(self) -> List[str]:
        return list(self.module_dict.keys())

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
                        module_rel_path = PythonASTIndexer._relative_module_path(
                            self.abs_path, module_path
                        )
                        module_dict[module_rel_path] = module
        return module_dict

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
    def _relative_module_path(root_abs_path, module_path) -> str:
        module_rel_path = (os.path.relpath(module_path, root_abs_path).replace(os.path.sep, "."))[
            :-3
        ]
        return module_rel_path

    @staticmethod
    def _overview_traverse_helper(node, line_items, num_spaces=1):
        if isinstance(node, ClassDef):
            line_items.append("  " * num_spaces + " - cls " + node.name)
        elif isinstance(node, FunctionDef) or isinstance(node, AsyncFunctionDef):
            line_items.append("  " * num_spaces + " - func " + node.name)

        for child in ast.iter_child_nodes(node):
            PythonASTIndexer._overview_traverse_helper(child, line_items, num_spaces + 1)
