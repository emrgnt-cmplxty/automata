"""
This module provides a Python Abstract Syntax Tree (AST) indexer to help retrieve code and docstrings from
Python source code files in a specified directory. The PythonASTIndexer class supports retrieval of code
and docstrings for top-level functions, methods, and classes.

Dependencies:
- os
- ast
- typing (Dict, Optional, Union, cast)

Classes:
PythonASTIndexer: Main class to index and retrieve code and docstrings from Python source files.

Example:
indexer = PythonASTIndexer("/path/to/python/source")
code = indexer.retrieve_code("module.path", "ClassName.method_name")
docstring = indexer.retrieve_docstring("module.path", "ClassName.method_name")
"""
import ast
import logging
import os
from ast import AsyncFunctionDef, ClassDef, FunctionDef, Module
from typing import Dict, Optional, Union, cast

logger = logging.getLogger(__name__)


class PythonASTIndexer:
    """
    A class to index Python source code files in a specified directory and retrieve code and docstrings.
    Attributes:
        root_dir (str): The root directory containing Python source code files to be indexed.
        module_dict (Dict[str, Module]): A dictionary with module paths as keys and AST Module objects as values.

    Methods:
        __init__(self, root_dir: str) -> None
        retrieve_code(self, module_path: str, object_path: Optional[str]) -> Optional[str]
        retrieve_docstring(self, module_path: str, object_path: Optional[str]) -> Optional[str]
    """

    NO_RESULT_FOUND_STR = "No Result Found."
    PATH_SEP = "."

    def __init__(self, root_dir: str) -> None:
        """
        Initializes the PythonASTIndexer with the specified root directory and builds the module dictionary.

        Args:
            root_dir (str): The root directory containing Python source code files to be indexed.
        """

        self.root_dir = root_dir
        self.module_dict = self._build_module_dict()

    def retrieve_code(self, module_path: str, object_path: Optional[str]) -> Optional[str]:
        """
        Retrieve code for a specified module, class, or function/method.

        Args:
            module_path (str): The path of the module in dot-separated format (e.g. 'package.module').
            object_path (Optional[str]): The path of the class, function, or method in dot-separated format
                (e.g. 'ClassName.method_name'). If None, the entire module code will be returned.

        Returns:
            Optional[str]: The code for the specified module, class, or function/method, or "No Result Found."
                if not found.
        """

        if module_path not in self.module_dict:
            return PythonASTIndexer.NO_RESULT_FOUND_STR

        module = self.module_dict[module_path]
        result = self._find_module_class_function_or_method(module, object_path)
        if result is not None:
            self._remove_docstrings(result)
            return ast.unparse(result)
        else:
            return PythonASTIndexer.NO_RESULT_FOUND_STR

    def retrieve_docstring(self, module_path: str, object_path: Optional[str]) -> Optional[str]:
        """
        Retrieve the docstring for a specified module, class, or function/method.

        Args:
            module_path (str): The path of the module in dot-separated format (e.g. 'package.module').
            object_path (Optional[str]): The path of the class, function, or method in dot-separated format
                (e.g. 'ClassName.method_name'). If None, the module-level docstring will be returned.

        Returns:
            Optional[str]: The docstring for the specified module, class, or function/method, or "No Result Found."
                if not found.
        """

        if module_path not in self.module_dict:
            return PythonASTIndexer.NO_RESULT_FOUND_STR

        module = self.module_dict[module_path]
        result = self._find_module_class_function_or_method(module, object_path)
        if result is not None:
            return ast.get_docstring(result)
        else:
            return PythonASTIndexer.NO_RESULT_FOUND_STR

    def _build_module_dict(self) -> Dict[str, Module]:
        """
        Builds the module dictionary by walking through the root directory and creating AST Module objects
        for each Python source file. The module paths are used as keys in the dictionary.

        Returns:
            Dict[str, Module]: A dictionary with module paths as keys and AST Module objects as values.
        """

        module_dict = {}

        for root, _, files in os.walk(self.root_dir):
            for file in files:
                if file.endswith(".py"):
                    module_path = os.path.join(root, file)
                    module = self._load_module_from_path(module_path)
                    if module:
                        module_rel_path = (
                            os.path.relpath(module_path, self.root_dir)
                            .replace(os.path.sep, ".")
                            .replace(".py", "")
                        )
                        module_dict[module_rel_path] = module
        return module_dict

    @staticmethod
    def _load_module_from_path(path) -> Optional[Module]:
        """
        Loads and returns an AST Module object for the given file path.

        Args:
            path (str): The file path of the Python source code.

        Returns:
            Module: The AST Module object for the given file path, or None if the module cannot be loaded.
        """

        try:
            module = ast.parse(open(path).read())
            return module
        except Exception as e:
            logger.error(f"Failed to load module '{path}' due to: {e}")
            return None

    @staticmethod
    def _find_module_class_function_or_method(
        code_obj: Union[Module, ClassDef], object_path: Optional[str]
    ) -> Optional[Union[FunctionDef, AsyncFunctionDef, ClassDef, Module]]:
        """
        Find a module, or find a function, method, or class inside a module.

        Args:
            code_obj (Union[Module, ClassDef]): The AST code object (Module or ClassDef) to search.
            object_path (Optional[str]): The dot-separated object path (e.g., 'ClassName.method_name'). If None,
                the module is returned.

        Returns:
            Optional[Union[FunctionDef, AsyncFunctionDef, ClassDef]]: The found FunctionDef,
                AsyncFunctionDef, or ClassDef node, or None if not found.
        """

        if object_path is None:
            assert isinstance(code_obj, Module)
            return cast(Module, code_obj)

        obj_parts = object_path.split(PythonASTIndexer.PATH_SEP)

        if len(obj_parts) == 1:
            return PythonASTIndexer._find_node(code_obj, obj_parts[0])
        elif len(obj_parts) == 2:
            class_node = PythonASTIndexer._find_node(code_obj, obj_parts[0])
            if class_node and isinstance(class_node, ClassDef):
                return PythonASTIndexer._find_node(class_node, obj_parts[1])
        return None

    @staticmethod
    def _find_node(
        code_obj: Union[Module, ClassDef], obj_name: str
    ) -> Optional[Union[FunctionDef, AsyncFunctionDef, ClassDef]]:
        """
        Find a FunctionDef, AsyncFunctionDef, or ClassDef node with the specified name within the given
        AST code object.

        Args:
            code_obj (Union[Module, ClassDef]): The AST code object (Module or ClassDef) to search.
            obj_name (str): The name of the object to find.

        Returns:
            Optional[Union[FunctionDef, AsyncFunctionDef, ClassDef]]: The found FunctionDef,
                AsyncFunctionDef, or ClassDef node, or None if not found.
        """

        for node in code_obj.body:
            if isinstance(node, FunctionDef) and node.name == obj_name:
                return node
            elif isinstance(node, ClassDef) and node.name == obj_name:
                return node
        return None

    @staticmethod
    def _remove_docstrings(result: Union[FunctionDef, AsyncFunctionDef, ClassDef, Module]):
        """
        Remove docstrings from the specified AST node and its child nodes (if any).

        Args:
            result (Union[FunctionDef, AsyncFunctionDef, ClassDef, Module]): The AST node
                to remove docstrings from.
        """

        if isinstance(result, (FunctionDef, AsyncFunctionDef, ClassDef)):
            if isinstance(result.body[0], ast.Expr) and isinstance(result.body[0].value, ast.Str):
                result.body.pop(0)

        if isinstance(result, ClassDef):
            for node in result.body:
                if (
                    isinstance(node, FunctionDef)
                    or isinstance(node, AsyncFunctionDef)
                    or isinstance(node, ClassDef)
                    or isinstance(node, Module)
                ):
                    PythonASTIndexer._remove_docstrings(node)

        if isinstance(result, Module):
            if isinstance(result.body[0], ast.Expr) and isinstance(result.body[0].value, ast.Str):
                result.body.pop(0)
            for node in result.body:
                if (
                    isinstance(node, FunctionDef)
                    or isinstance(node, AsyncFunctionDef)
                    or isinstance(node, ClassDef)
                    or isinstance(node, Module)
                ):
                    PythonASTIndexer._remove_docstrings(node)
