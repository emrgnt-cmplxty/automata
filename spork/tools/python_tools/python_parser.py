"""
PythonParser

This module provides functionality to extract information about classes, functions,
and their docstrings from a given directory of Python files. It defines the `PythonParser`
class that can be used to get the source code, docstrings, and list of functions
or classes within a specific file.

Example usage:
    parser = PythonParser()

    print("Fetch raw code of a function:")
    print(parser.get_raw_code('package_dir.module_name.function_name'))

    print("Fetch raw code of a method:")
    print(parser.get_raw_code('package_dir.module_name.ClassName.method_name'))

    print("Fetch the docstring summary of a package:")
    print(parser.get_docstring('package_dir'))

    TODO
    1. Consider how to handle import statements, they are not currently parsed.
    2. Include support for getting code + doc strings in a single shot
"""
import ast
import os
from typing import Any, Callable, Dict, List

from ..utils import home_path
from .python_types import (
    RESULT_NOT_FOUND,
    PythonClassType,
    PythonFunctionType,
    PythonModuleType,
    PythonPackageType,
)


class PythonParser:
    """
    The PythonParser class provides functionality to extract and access information about
    classes, functions, and their docstrings from a given directory of Python files.

    Attributes:
        module_dict (Dict[str, PythonModuleType]): A dictionary that maps file names to their corresponding PythonModuleType instances.
    """

    def __init__(self, relative_dir: str = "spork"):
        self.function_dict: Dict[str, PythonFunctionType] = {}
        self.class_dict: Dict[str, PythonClassType] = {}
        self.module_dict: Dict[str, PythonModuleType] = {}
        self.package_dict: Dict[str, PythonPackageType] = {}
        self.relative_dir = relative_dir
        self._populate_dicts(os.path.join(home_path(), self.relative_dir))
        self._update_callbacks: List[Callable[[str, str, Dict[str, Any]], None]] = []
        self.absolute_path_to_base = os.path.join(home_path(), self.relative_dir, "..")

    def get_raw_code(self, object_py_path: str) -> str:
        """
        Returns the raw code of a function, class, or module with the given name,
        or RESULT_NOT_FOUND if the PythonObjectType is not found.

        Args:
            object_py_path (str): The python path of the PythonObjectType (module, class, method, or function) to look up.

        Returns:
            str: The raw code of the PythonObjectType, or RESULT_NOT_FOUND if the PythonObjectType is not found.
        """
        if object_py_path in self.function_dict:
            return self.function_dict[object_py_path].get_raw_code()
        elif object_py_path in self.class_dict:
            return self.class_dict[object_py_path].get_raw_code()
        elif object_py_path in self.module_dict:
            return self.module_dict[object_py_path].get_raw_code()
        elif object_py_path in self.package_dict:
            return self.package_dict[object_py_path].get_raw_code()
        else:
            return RESULT_NOT_FOUND

    def get_docstring(self, object_py_path: str) -> str:
        """
        Returns the docstrings of a function, class, or module with the given name, or RESULT_NOT_FOUND.

        Args:
            object_py_path (str): The python path of the PythonObjectType (module, class, method, or function) to look up.

        Returns:
            str: The docstring code of the PythonObjectType, or RESULT_NOT_FOUND.
        """
        if object_py_path in self.function_dict:
            return self.function_dict[object_py_path].get_docstring()
        elif object_py_path in self.class_dict:
            return self.class_dict[object_py_path].get_docstring()
        elif object_py_path in self.module_dict:
            return self.module_dict[object_py_path].get_docstring()
        elif object_py_path in self.package_dict:
            return self.package_dict[object_py_path].get_docstring()
        else:
            return RESULT_NOT_FOUND

    def _populate_dicts(self, abs_dir: str) -> None:
        """
        Populates the file_dict, class_dict, and function_dict with PythonModuleType, PythonClassType, and PYthonFunctionType
        for each Python file found in the specified directory.

        Args:
            rel_dir (str): The absolute directory containing the Python files.
        """
        packages: Dict[str, Dict[str, PythonModuleType]] = {}
        for root, _dirs, files in os.walk(abs_dir):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    module_py_path = os.path.relpath(
                        file_path, os.path.join(abs_dir, "..")
                    ).replace(os.path.sep, ".")[:-3]

                    # Get the python path
                    package_name = ".".join(module_py_path.split(".")[:-1])

                    with open(file_path, "r", encoding="utf-8") as f:
                        node = ast.parse(f.read())

                    docstring = ast.get_docstring(node)
                    standalone_functions = []
                    classes = []
                    imports = []
                    for n in node.body:
                        if isinstance(n, (ast.Import, ast.ImportFrom)):
                            import_code = "".join(ast.unparse(n)).strip()
                            imports.append(import_code)
                        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
                            func_name = n.name
                            func_docstring = ast.get_docstring(n)
                            func_code = "".join(ast.unparse(n))
                            func_py_path = f"{module_py_path}.{func_name}"
                            function = PythonFunctionType(
                                func_py_path,
                                func_docstring if func_docstring else "",
                                func_code,
                            )
                            standalone_functions.append(function)
                            self.function_dict[func_py_path] = function
                        elif isinstance(n, ast.ClassDef):
                            class_name = n.name
                            class_docstring = ""

                            # Check for the __init__ method and extract its docstring
                            for stmt in n.body:
                                if (
                                    isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef))
                                    and stmt.name == "__init__"
                                ):
                                    class_docstring = ast.get_docstring(stmt) or RESULT_NOT_FOUND
                                    break
                            class_code = "".join(ast.unparse(n))
                            class_py_path = f"{module_py_path}.{class_name}"
                            class_obj = PythonClassType(
                                class_py_path,
                                class_docstring if class_docstring else RESULT_NOT_FOUND,
                                class_code,
                            )
                            classes.append(class_obj)
                            self.class_dict[class_py_path] = class_obj

                            # Adding class methods to function_dict
                            for m in n.body:
                                if isinstance(m, (ast.FunctionDef, ast.AsyncFunctionDef)):
                                    method_name = m.name
                                    method_docstring = ast.get_docstring(m)
                                    method_code = "".join(ast.unparse(m))
                                    method_py_path = f"{class_py_path}.{method_name}"
                                    method_obj = PythonFunctionType(
                                        method_py_path,
                                        method_docstring if method_docstring else RESULT_NOT_FOUND,
                                        method_code,
                                    )
                                    class_obj.methods[method_name] = method_obj
                                    self.function_dict[method_py_path] = method_obj
                    module_obj = PythonModuleType(
                        module_py_path,
                        docstring if docstring else RESULT_NOT_FOUND,
                        standalone_functions,
                        classes,
                        imports,
                    )

                    # Use the python path as the key
                    self.module_dict[module_py_path] = module_obj

                    if package_name not in packages:
                        packages[package_name] = {}
                    packages[package_name][module_py_path] = module_obj

        for package_name, modules in packages.items():
            self.package_dict[package_name] = PythonPackageType(package_name, modules)

    def register_update_callback(
        self, callback: Callable[[str, str, Dict[str, Any]], None]
    ) -> None:
        self._update_callbacks.append(callback)

    def _notify_update(self, object_type: str, py_path: str) -> None:
        for callback in self._update_callbacks:
            callback(object_type, py_path, {})


if __name__ == "__main__":
    python_parser = PythonParser()
    print("Done loading the Code Parser")
    print("Code Parser Raw Code:\n%s" % (python_parser.get_raw_code("spork.tools.code.parser")))
