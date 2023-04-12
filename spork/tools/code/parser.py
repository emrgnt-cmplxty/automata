"""
CodeParser

This module provides functionality to extract information about classes, functions,
and their docstrings from a given directory of Python files. It defines the `CodeParser`
class that can be used to get the source code, docstrings, and list of functions
or classes within a specific file.

Example usage:
    code_get = CodeParser(os.path.join(home_path(), "spork"))

    print("Docstring of a class or function:")
    print(code_get.get_docstring('module_dir.module_name.ClassName_Or_function_name'))

    print("Source code of a class or function:")
    print(code_get.get_raw_code('module_dir.module_name.ClassName_Or_function_name'))

    print("Standalone functions in a module:")
    print(code_get.get_module_standalone_functions('module_dir.module_name'))

    print("Classes in a file")
    print(code_get.get_module_classes('path/to/file/file_name.py'))

    print("Docstring of a file:")
    print(code_get.get_module_docstring('path/to/file/file_name.py'))
"""
import abc
import ast
import os
from typing import Dict, List, Optional, cast

from ..utils import home_path

RESULT_NOT_FOUND = "No results found."


class Object(abc.ABC):
    """
    The Object class represents a single object with its python path, docstring, and raw code.

    Attributes:
        py_path (str): The name of the object.
        docstring (str): The docstring of the object.
        code (str): The raw code of the object.
    """

    def __init__(self, py_path: str, docstring: str, code: str):
        self.py_path = py_path
        self.docstring = docstring
        self.code = code

    def get_raw_code(self) -> str:
        """
        Returns the raw code of the object.

        Note:
            This method may be extended by subclasses to customize the behavior.

        Returns:
            str: The raw code of the object as a string.
        """

        node = ast.parse(self.code)
        if isinstance(node.body[0], (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            node.body[0].body.pop(0)  # Remove the docstring node
        return ast.unparse(node)

    def get_doc_string(self) -> str:
        """
        Returns the docstring of the object.

        Note:
            This method may be extended by subclasses to customize the behavior.

        Returns:
            str: The docstring of the object as a string.
        """
        name = self.py_path.split(".")[-1]
        return f"{name}:\n{self.docstring}" if self.docstring else RESULT_NOT_FOUND


class FunctionObject(Object):
    """
    The FunctionObject class represents a single function (or method) with its python path, docstring, and raw code.

    Attributes:
        methods (Dict[str, FunctionObject]): A dictionary of associated FunctionObject instances, keyed by method names.
    """

    def __init__(self, py_path: str, docstring: str, code: str):
        super().__init__(py_path, docstring, code)


class ClassObject(Object):
    """
    The ClassObject class represents a single class with its python path, docstring, and raw code.

    Attributes:
        py_path (str): The name of the class.
        docstring (str): The docstring of the class.
        code (str): The raw code of the class.
        methods (Dict[str, FunctionObject]): A dictionary of associated FunctionObject instances, keyed by method names.
    """

    def __init__(self, py_path: str, docstring: str, code: str):
        super().__init__(py_path, docstring, code)
        self.methods = self._parse_methods()

    def get_raw_code(self, exclude_methods: bool = False) -> str:
        """
        Returns the raw code of the object without the docstring,
        and with methods' docstrings removed as well.

        Returns:
            str: The raw code of the object as a string.
        """
        node = ast.parse(self.code)
        if isinstance(node.body[0], ast.ClassDef):
            # Remove the class docstring node
            if isinstance(node.body[0].body[0], ast.Expr) and isinstance(
                node.body[0].body[0].value, ast.Str
            ):
                node.body[0].body.pop(0)

            # Iterate through the methods and remove their docstrings
            for method_node in node.body[0].body:
                if isinstance(method_node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    if (
                        isinstance(method_node.body[0], ast.Expr)
                        and isinstance(method_node.body[0].value, ast.Str)
                        or (exclude_methods and method_node.name != "__init__")
                    ):
                        method_node.body.pop(0)
        return ast.unparse(node)

    def get_doc_string(self, exclude_methods: bool = False) -> str:
        """
        Returns the docstring of the class.

        Returns:
            str: The docstring of the class as a string.
        """

        result = RESULT_NOT_FOUND
        if self.docstring:
            name = self.py_path.split(".")[-1]
            result = f"{name}:\n{self.docstring}"

        if not exclude_methods:
            for method in self.methods.values():
                if result == RESULT_NOT_FOUND:
                    result = ""
                result += f"\n{method.get_doc_string()}"

        return result

    def _parse_methods(self) -> Dict[str, FunctionObject]:
        """
        Parses the class code and extracts its methods as FunctionObject instances.

        Returns:
            Dict[str, FunctionObject]: A dictionary of associated FunctionObject instances, keyed by method names.
        """
        # Assuming self.code is an ast.ClassDef node
        class_node = cast(ast.ClassDef, ast.parse(self.code).body[0])
        methods = {}

        for n in class_node.body:
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
                func_name = n.name
                func_docstring = ast.get_docstring(n) or RESULT_NOT_FOUND
                func_code = ast.unparse(n)
                methods[func_name] = FunctionObject(func_name, func_docstring, func_code)

        return methods


class ModuleObject(Object):
    """
    The ModuleObject class represents a single python module with associated docstrings, standalone functions, and classes.

    Attributes:
        filepath (str): The filepath of the file.
        docstring (str): The docstring of the file.
        standalone_functions (List[FunctionObject]): A list of FunctionObject instances representing standalone functions.
        classes (List[FunctionObject]): A list of FunctionObject instances representing classes.
    """

    def __init__(
        self,
        py_path: str,
        docstring: str,
        standalone_functions: List[FunctionObject],
        classes: List[ClassObject],
    ):
        super().__init__(py_path, docstring, RESULT_NOT_FOUND)
        self.standalone_functions = standalone_functions
        self.classes = classes

    def get_raw_code(
        self, exclude_standalones: bool = False, exclude_methods: bool = False
    ) -> str:
        """
        Returns the raw code of the module, including all nested functions and classes.

        Args:
            exclude_standalones (bool): If True, exclude docstrings of standalone functions from the result.
            exclude_methods (bool): If True, exclude docstrings of methods from the result.

        Returns:
            str: The raw code of the module as a string.
        """
        raw_code = []
        if not exclude_standalones:
            for func_obj in self.standalone_functions:
                raw_code.append(func_obj.get_raw_code())
                raw_code.append("\n")

        for class_obj in self.classes:
            raw_code.append(class_obj.get_raw_code(exclude_methods))
            raw_code.append("\n")

        return "\n".join(raw_code) if len(raw_code) > 0 else RESULT_NOT_FOUND

    def get_docstring(self, exclude_standalones: bool = True, exclude_methods: bool = True) -> str:
        """
        Returns the concatenated docstrings of all nested functions and classes in the module.

        Args:
            exclude_standalones (bool): If True, exclude docstrings of standalone functions from the result.
            exclude_methods (bool): If True, exclude docstrings of methods from the result.

        Returns:
            str: The concatenated docstrings of the module as a string.
        """

        docstrings = []
        if self.docstring:
            name = self.py_path.split(".")[-1]
            docstrings.append(f"{name}:\n{self.docstring}")

        if not exclude_standalones:
            for func_obj in self.standalone_functions:
                docstrings.append(func_obj.get_doc_string())
                docstrings.append("\n")

        for class_obj in self.classes:
            docstrings.append(class_obj.get_doc_string(exclude_methods))
            docstrings.append("\n")

        return "\n".join(docstrings) if len(docstrings) > 0 else RESULT_NOT_FOUND


class PackageObject(Object):
    def __init__(self, py_path: str, modules: Dict[str, ModuleObject]):
        super().__init__(py_path, RESULT_NOT_FOUND, RESULT_NOT_FOUND)
        self.modules = modules

    def get_docstring(self, exclude_standalones: bool = True, exclude_methods: bool = True) -> str:
        """
        Returns the concatenated docstrings of all modules inside the package.

        Args:
            exclude_standalones (bool): If True, exclude docstrings of standalone functions from the result.
            exclude_methods (bool): If True, exclude docstrings of methods from the result.

        Returns:
            str: The concatenated docstrings of the module as a string.
        """

        docstrings = []
        for module in self.modules.values():
            docstrings.append(module.get_docstring(exclude_standalones, exclude_methods))
        return "\n".join(docstrings) if len(docstrings) > 0 else RESULT_NOT_FOUND

    def get_raw_code(
        self, exclude_standalones: bool = False, exclude_methods: bool = False
    ) -> str:
        """
        Returns the raw code of the module, including all nested functions and classes.

        Args:
            exclude_standalones (bool): If True, exclude code of standalone functions in modules from the result.
            exclude_methods (bool): If True, exclude code of methods from the result.

        Returns:
            str: The concatenated raw code of the module as a string.
        """

        raw_code = []
        for module in self.modules.values():
            raw_code.append(module.get_raw_code(exclude_standalones, exclude_methods))
        return "\n".join(raw_code) if len(raw_code) > 0 else RESULT_NOT_FOUND


class CodeParser:
    """
    The CodeParser class provides functionality to extract and access information about
    classes, functions, and their docstrings from a given directory of Python files.

    Attributes:
        module_dict (Dict[str, ModuleObject]): A dictionary that maps file names to their corresponding ModuleObject instances.
    """

    def __init__(self, root_dir: Optional[str] = None):
        self.function_dict: Dict[str, FunctionObject] = {}
        self.class_dict: Dict[str, ClassObject] = {}
        self.module_dict: Dict[str, ModuleObject] = {}
        self.package_dict: Dict[str, PackageObject] = {}
        self._populate_dicts(root_dir if root_dir else os.path.join(home_path(), "spork"))
        print("package_dict = ", self.package_dict)

    def get_raw_code(self, object_py_path: str) -> str:
        """
        Returns the raw code of a function, class, or module with the given name,
        or RESULT_NOT_FOUND if the object is not found.

        Args:
            object_py_path (str): The python path of the object (module, class, method, or function) to look up.

        Returns:
            str: The raw code of the object, or RESULT_NOT_FOUND if the object is not found.
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
            object_py_path (str): The python path of the object (module, class, method, or function) to look up.

        Returns:
            str: The docstring code of the object, or RESULT_NOT_FOUND.
        """
        if object_py_path in self.function_dict:
            return self.function_dict[object_py_path].get_doc_string()
        elif object_py_path in self.class_dict:
            return self.class_dict[object_py_path].get_doc_string()
        elif object_py_path in self.module_dict:
            return self.module_dict[object_py_path].get_docstring()
        elif object_py_path in self.package_dict:
            return self.package_dict[object_py_path].get_docstring()
        else:
            return RESULT_NOT_FOUND

    def _populate_dicts(self, root_dir: str) -> None:
        """
        Populates the file_dict, class_dict, and function_dict with ModuleObjects, ClassObjects, and FunctionObjects
        for each Python file found in the specified directory.

        Args:
            root_dir (str): The root directory containing the Python files.
        """
        packages: Dict[str, Dict[str, ModuleObject]] = {}
        for root, _dirs, files in os.walk(root_dir):
            for file in files:
                if file.endswith(".py"):
                    if file == "__init__.py":
                        continue
                    file_path = os.path.join(root, file)
                    module_py_path = os.path.relpath(file_path, root_dir).replace(
                        os.path.sep, "."
                    )[
                        :-3
                    ]  # Get the python path
                    package_name = ".".join(module_py_path.split(".")[:-1])

                    with open(file_path, "r", encoding="utf-8") as f:
                        node = ast.parse(f.read())

                    docstring = ast.get_docstring(node)
                    standalone_functions = []
                    classes = []
                    for n in node.body:
                        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
                            func_name = n.name
                            func_docstring = ast.get_docstring(n)
                            func_code = "".join(ast.unparse(n))
                            func_py_path = f"{module_py_path}.{func_name}"
                            function = FunctionObject(
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
                            class_obj = ClassObject(
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
                                    method_obj = FunctionObject(
                                        method_py_path,
                                        method_docstring if method_docstring else RESULT_NOT_FOUND,
                                        method_code,
                                    )
                                    class_obj.methods[method_name] = method_obj
                                    self.function_dict[method_py_path] = method_obj
                    module_obj = ModuleObject(
                        module_py_path,
                        docstring if docstring else RESULT_NOT_FOUND,
                        standalone_functions,
                        classes,
                    )

                    # Use the python path as the key
                    self.module_dict[module_py_path] = module_obj

                    if package_name not in packages:
                        packages[package_name] = {}
                    packages[package_name][module_py_path] = module_obj

        for package_name, modules in packages.items():
            self.package_dict[package_name] = PackageObject(package_name, modules)
