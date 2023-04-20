"""
This module provides a Python Abstract Syntax Tree (AST) indexer to help retrieve code and docstrings from
Python source code files in a specified directory. The PythonIndexer class supports retrieval of code
and docstrings for top-level functions, methods, and classes.

Dependencies:
- os
- ast
- typing (Dict, Optional, Union, cast)

Classes:
PythonIndexer: Main class to index and retrieve code and docstrings from Python source files.

Example:
indexer = PythonIndexer("/path/to/python/source")
code = indexer.retrieve_code("module.path", "ClassName.method_name")
docstring = indexer.retrieve_docstring("module.path", "ClassName.method_name")
"""
import ast
import logging
import os
import textwrap
from ast import AsyncFunctionDef, ClassDef, FunctionDef, Module
from typing import Dict, Optional, Union, cast
from spork.tools.utils import root_path

logger = logging.getLogger(__name__)


class PythonIndexer:
    """
    A class to index Python source code files in a specified directory and retrieve code and docstrings.
    Attributes:
        rel_path (str): The relative path to the root directory containing Python source code files to be indexed.
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
        print("self.abs_path = ", self.abs_path)
        self.module_dict = self._build_module_dict()
        print("self.module_dict = ", self.module_dict)
        # get file path
        self.absolute_path_to_base = os.path.abspath(__file__)
        print("self.absolute_path_to_base = ", self.absolute_path_to_base)

    def retrieve_code(self, module_path: str, object_path: Optional[str]) -> str:
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
        result = self._find_module_class_function_or_method(module, object_path)
        if result is not None:
            self._remove_docstrings(result)
            return ast.unparse(result)
        else:
            return PythonIndexer.NO_RESULT_FOUND_STR

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
        result = self._find_module_class_function_or_method(module, object_path)
        if result is not None:
            return ast.get_docstring(result)
        else:
            return PythonIndexer.NO_RESULT_FOUND_STR

    def get_module_path(self, module_obj: Module) -> str:
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

    def get_overview(self, print_func_docstrings=False, print_method_docstrings=False) -> str:
        """
        Loops over the PythonParser's dictionaries and returns a string that provides an overview of the PythonParser's state.
        Returns:
            str: A string that provides an overview of the PythonParser's state.
        """
        result = ""
        LINE_SPACING = 2
        return "x"
        # for package in self.package_dict.values():
        #     for module in package.modules.values():
        #         if "type" in module.py_path.split(".")[-1]:
        #             continue
        #         if (
        #             len(module.classes.keys()) == 0
        #             and len(module.standalone_functions.keys()) == 0
        #         ):
        #             continue
        #         result += module.py_path + "\n"
        #         if len(module.standalone_functions.keys()) > 0:
        #             for function in module.standalone_functions.values():
        #                 if "_" == function.py_path.split(".")[-1][0]:
        #                     continue
        #                 function_name = function.py_path.split(".")[-1]
        #                 result += textwrap.indent(function_name, " " * LINE_SPACING * 1) + "\n"
        #                 if print_func_docstrings:
        #                     result += (
        #                         textwrap.indent(
        #                             "\n".join(function.get_docstring().split("\n")[1:]),
        #                             " " * LINE_SPACING * 2,
        #                         )
        #                         + "\n"
        #                     )
        #         if len(module.classes) > 0:
        #             for class_obj in module.classes.values():
        #                 class_name = class_obj.py_path.split(".")[-1]
        #                 result += textwrap.indent(class_name, " " * LINE_SPACING * 1) + "\n"
        #                 if len(list(class_obj.methods.keys())) > 0:
        #                     for method in class_obj.methods.values():
        #                         if "_" == method.py_path.split(".")[-1][0]:
        #                             continue
        #                         module_name = method.py_path.split(".")[-1]
        #                         result += (
        #                             textwrap.indent(module_name, " " * LINE_SPACING * 2) + "\n"
        #                         )
        #                         if print_method_docstrings:
        #                             result += (
        #                                 textwrap.indent(
        #                                     "\n".join(method.get_docstring().split("\n")[1:]),
        #                                     " " * LINE_SPACING * 3,
        #                                 )
        #                                 + "\n"
        #                             )
        # return result

    def _build_module_dict(self) -> Dict[str, Module]:
        """
        Builds the module dictionary by walking through the root directory and creating AST Module objects
        for each Python source file. The module paths are used as keys in the dictionary.

        Returns:
            Dict[str, Module]: A dictionary with module paths as keys and AST Module objects as values.
        """

        module_dict = {}

        for root, _, files in os.walk(self.abs_path):
            for file in files:
                if file.endswith(".py"):
                    module_path = os.path.join(root, file)
                    module = self._load_module_from_path(module_path)
                    if module:
                        module_rel_path = (
                            os.path.relpath(module_path, self.abs_path)
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

        obj_parts = object_path.split(PythonIndexer.PATH_SEP)

        if len(obj_parts) == 1:
            return PythonIndexer._find_node(code_obj, obj_parts[0])
        elif len(obj_parts) == 2:
            class_node = PythonIndexer._find_node(code_obj, obj_parts[0])
            if class_node and isinstance(class_node, ClassDef):
                return PythonIndexer._find_node(class_node, obj_parts[1])
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
                    PythonIndexer._remove_docstrings(node)

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
                    PythonIndexer._remove_docstrings(node)
