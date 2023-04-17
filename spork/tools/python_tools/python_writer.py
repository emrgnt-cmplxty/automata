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
from typing import Any, Dict, List, Set, Tuple

from .python_parser import PythonParser
from .python_types import (
    RESULT_NOT_FOUND,
    PythonClassType,
    PythonFunctionType,
    PythonModuleType,
    PythonPackageType,
)


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
        self.modified_modules: Set[str] = set([])

    def modify_code_state(self, module_py_path: str, code: str) -> str:
        """
        This function takes the input path and code and intelligently determines whether this
        is a function, class, module, or package update. It then calls the appropriate method
        to perform the update.

        Args:
            module_py_path (str): The path to the Python file.
            code (str): The source code to be analyzed and updated.

        Raises:
            ValueError: If the provided code is not valid Python.
        """

        # Check that we can parse the code
        self._validate_code(code)

        package_path = module_py_path.split(".")[-1]

        # Create the package if it does not already exist
        if package_path not in self.python_parser.package_dict:
            self._create_new_package(package_path)

        # Update the module dictionaries
        if module_py_path not in self.python_parser.module_dict:
            self._create_new_module(module_py_path, code)
        else:
            self._modify_existing_module_imports(module_py_path, code)
        module = self.python_parser.module_dict[module_py_path]
        # Update the package dictionaries to reflect module changes
        self._modify_existing_package(package_path, module_py_path, module)
        print("code = ", code)

        # Update the class and function dictionaries
        class_methods, functions_dict, classes_code, _ = self.python_parser.parse_raw_code(code)
        print("class_methods = ", class_methods)
        print("classes_code = ", classes_code)
        for class_name in classes_code:
            class_path = f"{module_py_path}.{class_name}"
            print("updaing class_path = ", class_path)
            # Create the class entry if it does not already exist
            if class_path not in self.python_parser.class_dict:
                self._create_new_class(class_path, classes_code[class_name])

            # Update the class and function dictionaries
            for method_name in class_methods[class_name]:
                method_path = f"{class_path}.{method_name}"
                function = PythonFunctionType.from_code(
                    method_path, class_methods[class_name][method_name]
                )
                self.python_parser.class_dict[class_path].methods[method_path] = function
                self.python_parser.function_dict[method_path] = function
        for function_name in functions_dict:
            function_path = f"{module_py_path}.{function_name}"
            function_code = functions_dict[function_name]
            self.python_parser.function_dict[function_path] = PythonFunctionType.from_code(
                function_path, function_code
            )

        return "Success"

    def write_to_disk(self) -> str:
        """
        Rebuilds the Python module file at the given file path in a deterministic order,
        checking if the resulting output is a valid Python file.

        Raises:
            ValueError: If the resulting output is not a valid Python file.
        """
        for module_py_path in self.python_parser.module_dict.keys():
            file_path = os.path.join(
                self.python_parser.absolute_path_to_base, *(module_py_path.split("."))
            )
            if module_py_path in self.modified_modules:
                self._write_file(f"{file_path}.py", module_py_path)
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

        if docstring and docstring != RESULT_NOT_FOUND:
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
        subprocess.run(["isort", file_path])

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

    def _create_new_package(self, py_path: str) -> None:
        """
        Add a new package to the PythonParser package dictionary and update dependent dictionaries.

        Args:
            py_path (str): Package path.
        """
        assert py_path not in self.python_parser.package_dict
        self.python_parser.package_dict[py_path] = PythonPackageType(py_path, {})

    def _modify_existing_package(
        self, package_py_path: str, module_py_path: str, module: PythonModuleType
    ) -> None:
        """
        Modify an existing package in the PythonParser.

        Args:
            py_path (str): The Python path of the package to modify.
        """
        assert package_py_path in self.python_parser.package_dict
        self.python_parser.package_dict[package_py_path].modules[module_py_path] = module

    def _create_new_module(self, module_py_path: str, module_code: str) -> None:
        """
        Add a new module to the PythonParser.

        Args:
            module_py_path (str): The Python path of the module.
            module_code (str): The source code of the module.
        """
        assert module_py_path not in self.python_parser.module_dict
        stripped_module_code, import_statements = self._strip_import_statements(module_code)

        module_obj = PythonModuleType.from_code(
            module_py_path, stripped_module_code, import_statements
        )

        self.python_parser.module_dict[module_py_path] = module_obj
        self.modified_modules.add(module_py_path)

    def _modify_existing_module_imports(self, module_py_path: str, module_code: str) -> None:
        """
        Modify an existing module in the PythonParser.

        Args:
            module_py_path (str): The Python path of the module to modify.
            module_code (str): The new source code of the module.
        """
        assert module_py_path in self.python_parser.module_dict

        _, import_statements = self._strip_import_statements(module_code)
        self.python_parser.module_dict[module_py_path].imports.extend(import_statements)

    def _create_new_class(self, class_py_path: str, class_code: str) -> None:
        """
        Add a new class to the PythonParser.
        Args:
            module_py_path (str): The Python path of the module containing the class.
            class_py_path (str): The Python path of the class.
            class_code (str): The source code of the class.
            module_code (str, optional): The source code of the module, required if the module doesn't exist.
        """
        stripped_class_code, _ = self._strip_import_statements(class_code)
        class_obj = PythonClassType.from_code(class_py_path, stripped_class_code)
        self.python_parser.class_dict[class_py_path] = class_obj

    # TODO - Implement callbacks here for the PythonParser to use
    def _handle_update_notification(
        self, object_type: str, py_path: str, payload: Dict[str, Any]
    ) -> None:
        pass

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
        stripped_code_module = ast.Module(body=new_body, type_ignores=[])
        imports_module = ast.Module(body=import_statements, type_ignores=[])

        stripped_code = ast.unparse(stripped_code_module).strip()
        imports_code = ast.unparse(imports_module).strip()
        return stripped_code, [ele.strip() for ele in imports_code.split("\n")]
