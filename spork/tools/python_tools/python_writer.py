'''
PythonWriter

This module provides functionality to modify the in-memory representation 
of a Python package, via the PythonParser class, and write the changes to disk.

Example usage:
    parser = PythonParser()
    writer = PythonWriter(parser)

    print("Write a new standalone function:")
    print(writer.modify_code_state('package_dir.module_name.function_name', 'def function_name():\n"""A new function"""\npass'))

    print("Modify an existing function:")
    print(writer.modify_code_state('package_dir.module_name.function_name', 'def function_name():\n"""My Modified function"""\ndo_something()'))

    # The structure above works for packages, modules, classes, and methods as well.
    # when done modifying code, write the changes to disk:
    writer.write_to_disk()

    TODO
    1. Consider how to handle import statements, they are not currently parsed.
'''
import ast
import os
import subprocess
from typing import Any, Dict, List, Tuple

import astunparse

from .python_parser import PythonParser
from .python_types import PythonClassType, PythonFunctionType, PythonModuleType, PythonPackageType


class PythonWriter:
    """
    The PythonWriter class provides functionality to modify the in-memory representation
    of a Python package, via the PythonParser class, and write the changes to disk.

    Attributes:
        python_parser (PythonParser): An instance of PythonParser.

    """

    def __init__(self, python_parser: PythonParser):
        """
        Initialize PythonWriter with a PythonParser instance and register a callback for update notifications.

        Args:
            python_parser (PythonParser): An instance of PythonParser.
        """
        self.python_parser = python_parser
        self.python_parser.register_update_callback(self._handle_update_notification)

    def modify_code_state(self, py_path: str, code: str) -> str:
        """
        This function takes the input path and code and intelligently determines whether this
        is a function, class, module, or package update. It then calls the appropriate method
        to perform the update.

        Args:
            py_path (str): The path to the Python file.
            code (str): The source code to be analyzed and updated.

        Raises:
            ValueError: If the provided code is not valid Python.
        """

        has_class, has_function, has_module_docstring = self._get_code_type(py_path, code)

        if has_module_docstring:
            self._modify_or_create_new_module(py_path, code)
        elif has_class and not has_function:
            self._modify_or_create_new_class(py_path, code)
        elif has_function and not has_class:
            self._modify_or_create_new_function(py_path, code, has_class=False)
        elif has_function and has_class:
            self._modify_or_create_new_function(py_path, code, has_class=True)
        else:
            if "__init__" in py_path:
                self._modify_or_create_new_package(py_path, code)
            else:
                raise ValueError("Invalid code: Unable to determine the code type.")
        return "Success"

    def write_to_disk(self) -> str:
        """
        Rebuilds the Python module file at the given file path in a deterministic order,
        checking if the resulting output is a valid Python file.

        Raises:
            ValueError: If the resulting output is not a valid Python file.
        """

        for module_path in self.python_parser.module_dict.keys():
            file_path = os.path.join(
                self.python_parser.absolute_path_to_base, *(module_path.split("."))
            )
            self._write_file(f"{file_path}.py", module_path)
        return "Success"

    def _write_file(self, file_path: str, module_py_path: str) -> None:
        """
        Write the code for a module to a file.

        Args:
            file_path (str): The path to the file to write.
            module_py_path (str): The Python path of the module to write.

        Raises:
            ValueError: If the generated code is not valid Python.
        """
        module_obj = self.python_parser.module_dict[module_py_path]
        docstring = module_obj.docstring
        functions = module_obj.standalone_functions
        classes = module_obj.classes

        code_parts = []

        if docstring:
            code_parts.append(f'"""{docstring}"""\n\n')

        for import_statement in module_obj.imports:
            code_parts.append(import_statement)
            code_parts.append("\n")

        for function in functions:
            code_parts.append(function.code)
            code_parts.append("\n\n")

        for class_obj in classes:
            code_parts.append(class_obj.code)
            code_parts.append("\n\n")

        new_code = "".join(code_parts)

        try:
            ast.parse(new_code)
        except SyntaxError as e:
            raise ValueError(f"Generated code is not valid Python: {e}")
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_code)

        # Format the output file to match the Black style
        subprocess.run(["black", file_path])

    def _validate_code(self, code: str) -> None:
        """
        Validate the given Python code by parsing it and raising a ValueError if it's not valid.

        Args:
            code (str): Python code to validate.

        Raises:
            ValueError: If the provided code is not valid Python.
        """
        try:
            ast.parse(code)
        except SyntaxError as e:
            raise ValueError(f"Provided code is not valid Python: {e}")

    def _modify_or_create_new_function(
        self, function_py_path: str, function_code: str, has_class: bool
    ) -> None:
        """
        Add a new function to the PythonParser or modify an existing function.

        Args:
            function_py_path (str): The Python path of the function.
            function_code (str): The source code of the function.

        Raises:
            ValueError: If the provided code is not valid Python.
        """
        if function_py_path not in self.python_parser.function_dict:
            self._create_new_function(function_py_path, function_code, has_class)
        else:
            self._modify_existing_function(function_py_path, function_code)

    def _modify_or_create_new_class(self, class_py_path: str, class_code: str) -> None:
        """
        Add a new class to the PythonParser or modify an existing class.

        Args:
            class_py_path (str): The Python path of the class.
            class_code (str): The source code of the class.

        Raises:
            ValueError: If the provided code is not valid Python.
        """
        module_path = ".".join(class_py_path.split(".")[:-1])
        if class_py_path not in self.python_parser.class_dict:
            self._create_new_class(module_path, class_py_path, class_code)
        else:
            self._modify_existing_class(class_py_path, class_code)

    def _modify_or_create_new_module(self, module_py_path: str, module_code: str) -> None:
        """
        Add a new module to the PythonParser or modify an existing module.

        Args:
            module_py_path (str): The Python path of the module.
            module_code (str): The source code of the module.

        Raises:
            ValueError: If the provided code is not valid Python.
        """
        if module_py_path not in self.python_parser.module_dict:
            self._create_new_module(module_py_path, module_code)
        else:
            self._modify_existing_module(module_py_path, module_code)

    def _modify_or_create_new_package(self, package_py_path: str, package_code: str) -> None:
        """
        Add a new package to the PythonParser or modify an existing package.

        Args:
            package_py_path (str): The Python path of the package.
            package_code (str): The source code of the package.

        Raises:
            ValueError: If the provided code is not valid Python.
        """
        if package_py_path not in self.python_parser.package_dict:
            self._create_new_package(package_py_path)
        else:
            self._modify_existing_package(package_py_path, package_code)

    def _create_new_function(
        self, function_py_path: str, function_code: str, has_class: bool
    ) -> None:
        """
        Add a new function to the PythonParser.

        Args:
            function_py_path (str): The Python path of the function.
            code (str): The source code of the function.
        """

        stripped_function_code, import_statements = self._strip_import_statements(function_code)
        function_obj = PythonFunctionType.from_code(function_py_path, stripped_function_code)
        self.python_parser.function_dict[function_py_path] = function_obj

        if has_class:
            module_path = ".".join(function_py_path.split(".")[:-2])
            class_path = ".".join(function_py_path.split(".")[:-1])
            self.python_parser.class_dict[class_path].methods[function_obj.py_path] = function_obj
        else:
            module_path = ".".join(function_py_path.split(".")[:-1])
            self.python_parser.module_dict[module_path].standalone_functions.append(function_obj)

        self.python_parser.module_dict[module_path].imports.extend(import_statements)

    def _create_new_class(
        self, module_py_path: str, class_py_path: str, class_code: str, module_code=None
    ) -> None:
        """
        Add a new class to the PythonParser.

        Args:
            module_py_path (str): The Python path of the module containing the class.
            class_py_path (str): The Python path of the class.
            class_code (str): The source code of the class.
            module_code (str, optional): The source code of the module, required if the module doesn't exist.
        """
        stripped_class_code, import_statements = self._strip_import_statements(class_code)

        if module_py_path not in self.python_parser.module_dict:
            assert (
                module_code is not None
            ), "Module code must be provided if module does not exist."
            self._create_new_module(module_py_path, module_code)
        else:
            class_obj = PythonClassType.from_code(class_py_path, stripped_class_code)
            self.python_parser.class_dict[class_py_path] = class_obj
            self._update_dependent_dicts_on_class_creation(class_obj)

        print(
            "self.python_parser.module_dict[module_py_path] = ",
            self.python_parser.module_dict[module_py_path],
        )
        print(
            "self.python_parser.module_dict[module_py_path].imports = ",
            self.python_parser.module_dict[module_py_path].imports,
        )
        self.python_parser.module_dict[module_py_path].imports.extend(import_statements)

    def _create_new_module(self, module_py_path: str, module_code: str) -> None:
        """
        Add a new module to the PythonParser.

        Args:
            module_py_path (str): The Python path of the module.
            module_code (str): The source code of the module.
        """
        package_py_path = ".".join(module_py_path.split(".")[:-1])
        if package_py_path not in self.python_parser.package_dict:
            self._create_new_package(package_py_path)

        assert module_py_path not in self.python_parser.module_dict
        stripped_module_code, import_statements = self._strip_import_statements(module_code)

        module_obj = PythonModuleType.from_code(
            module_py_path, stripped_module_code, import_statements
        )

        self.python_parser.module_dict[module_py_path] = module_obj
        self._update_dependent_dicts_on_module_creation(module_obj)

    def _create_new_package(self, py_path: str) -> None:
        """
        Add a new package to the PythonParser package dictionary and update dependent dictionaries.

        Args:
            py_path (str): Package path.
            code (str): Python code for the package.
        """
        assert py_path not in self.python_parser.package_dict
        self.python_parser.package_dict[py_path] = PythonPackageType(py_path, {})

    def _modify_existing_function(self, function_py_path: str, function_code: str) -> None:
        """
        Modify an existing function in the PythonParser.

        Args:
            function_py_path (str): The Python path of the function to modify.
            function_code (str): The new source code of the function.

        Raises:
            ValueError: If the function is not found in the PythonParser's function_dict.
        """
        if function_py_path not in self.python_parser.function_dict:
            raise ValueError(f"Method or function {function_py_path} not found in function_dict.")
        old_function_obj = self.python_parser.function_dict[function_py_path]
        function_obj = PythonFunctionType.from_code(function_py_path, function_code)
        self.python_parser.function_dict[function_py_path] = function_obj
        # Update the class's method dict
        for class_key, class_obj in self.python_parser.class_dict.items():
            for method_key, method_obj in class_obj.methods.items():
                if method_obj == old_function_obj:
                    self.python_parser.class_dict[class_key].methods[method_key] = function_obj
                    break

    def _modify_existing_class(self, class_py_path: str, class_code: str) -> None:
        """
        Modify an existing class in the PythonParser.

        Args:
            class_py_path (str): The Python path of the class to modify.
            class_code (str): The new source code of the class.

        Raises:
            ValueError: If the class is not found in the PythonParser's class_dict.
        """
        if class_py_path not in self.python_parser.class_dict:
            raise ValueError(f"Class {class_py_path} not found in class_dict.")
        class_obj = PythonClassType.from_code(class_py_path, class_code)

        for method in class_obj.methods.values():
            self._modify_or_create_new_function(method.py_path, method.code, has_class=True)

        self.python_parser.class_dict[class_py_path] = class_obj

    def _modify_existing_module(self, module_py_path: str, module_code: str) -> None:
        """
        Modify an existing module in the PythonParser.

        Args:
            module_py_path (str): The Python path of the module to modify.
            module_code (str): The new source code of the module.

        Raises:
            ValueError: If the module is not found in the PythonParser's module_dict.
        """
        if module_py_path not in self.python_parser.module_dict:
            raise ValueError(f"Module {module_py_path} not found in module_dict.")

        stripped_module_code, import_statements = self._strip_import_statements(module_code)
        module_obj = PythonModuleType.from_code(
            module_py_path, stripped_module_code, import_statements
        )

        for class_obj in module_obj.classes:
            self._modify_existing_class(class_obj.py_path, class_obj.code)

        self.python_parser.module_dict[module_py_path] = module_obj

    def _modify_existing_package(self, _package_py_path: str, _package_code: str) -> None:
        """
        Modify an existing package in the PythonParser.

        Args:
            _package_py_path (str): The Python path of the package to modify.
            _package_code (str): The new source code of the package.

        Raises:
            ValueError: If called, as this method is not implemented.
        """

        raise NotImplementedError

    def _update_dependent_dicts_on_module_creation(self, module_obj: PythonModuleType) -> None:
        """
        Update the PythonParser's dependent dictionaries on the creation of a new module.

        Args:
            module_obj (PythonModuleType): The new module.

        Raises:
            ValueError: If the module's package is not found in the PythonParser's package_dict.
        """
        # Update the package dictionary based on the module path
        module_path = module_obj.py_path
        package_path = ".".join(module_path.split(".")[:-1])
        if package_path in self.python_parser.package_dict:
            self.python_parser.package_dict[package_path].modules[module_path] = module_obj

        for func_obj in module_obj.standalone_functions:
            self.python_parser.function_dict[func_obj.py_path] = func_obj

        for class_obj in module_obj.classes:
            self._update_dependent_dicts_on_class_creation(class_obj)

    def _update_dependent_dicts_on_class_creation(self, class_obj: PythonClassType) -> None:
        """
        Update the PythonParser's dependent dictionaries on the creation of a new class.

        Args:
            class_obj (PythonClassType): The new class.

        Raises:
            ValueError: If the class's module is not found in the PythonParser's module_dict.
        """
        class_py_path = class_obj.py_path
        self.python_parser.class_dict[class_py_path] = class_obj
        for method_obj in class_obj.methods.values():
            print("method_obj = ", method_obj)
            self.python_parser.function_dict[method_obj.py_path] = method_obj

    # TODO - Implement callbacks here for the PythonParser to use
    def _handle_update_notification(
        self, object_type: str, py_path: str, payload: Dict[str, Any]
    ) -> None:
        pass

    @staticmethod
    def _get_code_type(py_path: str, code: str) -> Tuple[bool, bool, bool]:
        """
        Determine the type of code at a given py_path, functions, and module-level docstrings in the given code.

        Args:
            py_path (str): The path to the Python file.
            code (str): The source code to be analyzed.

        Returns:
            Tuple[bool, bool, bool]: A tuple containing three boolean values.
                The first value indicates whether a class is present in the code.
                The second value indicates whether a function is present in the code.
                The third value indicates whether a module-level docstring is present in the code.
        """
        is_package = "__init__" in py_path
        if is_package:
            return False, False, False

        has_class = False
        has_function = False
        has_module_docstring = False

        code_ast = ast.parse(code)
        for node in code_ast.body:
            if isinstance(node, ast.FunctionDef):
                has_function = True
            elif isinstance(node, ast.ClassDef):
                has_class = True
            elif isinstance(node, ast.Expr) and isinstance(node.value, ast.Str):
                has_module_docstring = True

        return has_class, has_function, has_module_docstring

    @staticmethod
    def _strip_import_statements(code: str) -> Tuple[str, List[str]]:
        """
        Strip import statements from a given code string.

        Args:
            code (str): The code to be stripped.

        Returns:
            str: The stripped code.
            imports: The imports that were stripped.
        """
        # Parse the input code
        node = ast.parse(code)

        # Filter out import statements from the body
        new_body = [n for n in node.body if not isinstance(n, (ast.Import, ast.ImportFrom))]

        # Select the import statements exclusively
        import_statements = [n for n in node.body if isinstance(n, (ast.Import, ast.ImportFrom))]

        # Replace the original body with the filtered body
        node.body = new_body

        # Unparse the modified AST back to code
        stripped_code = astunparse.unparse(node).strip()
        imports_code = astunparse.unparse(import_statements).strip()
        return stripped_code, [ele.strip() for ele in imports_code.split("\n")]
