"""
PythonWriter - A utility class for manipulating with Python AST nodes.

This class provides methods for creating AST nodes from source code strings, and updating existing module objects with new code.
It also allows for extending and reducing module functionality by adding, updating or removing classes, methods, and functions.

Example usage:

    ast_wrapper = PythonWriter()

    # Extend a module with new or updated code
    code_to_extend = '''
    def new_function():
        print("New function added")

    class ExistingClass:
        def new_method(self):
            print("New method added")
    '''
    extended_module = ast_wrapper.extend_module(code_to_extend, extending_module=True, module_obj=existing_module)

    # Reduce a module by removing code
    code_to_reduce = '''
    def function_to_remove():
        pass

    class ClassToRemove:
        pass
    '''
    reduced_module = ast_wrapper.update_module(code_to_reduce, extending_module=False, module_obj=existing_module)

    TODO - Add explicit check of module contents after extension and reduction.
"""
import ast
import os
import re
import subprocess
from ast import ClassDef, FunctionDef, Import, ImportFrom, Module
from typing import Optional, Union, cast

from spork.tools.python_tools.python_indexer import PythonIndexer


class PythonWriter:
    """
    A utility class for working with Python AST nodes.

    Public Methods:

        update_module(
            source_code: str,
            extending_module: bool,
            module_obj (Optional[Module], keyword),
            module_path (Optional[str], keyword)
        ) -> None:
            Perform an in-place extention or reduction of a module object according to the received code.

        write_module(self) -> None:
            Write the module object to a file.

        Exceptions:
            ModuleNotFound: Raised when a module cannot be found.
            InvalidArguments: Raised when invalid arguments are passed to a method.
    """

    class ModuleNotFound(Exception):
        pass

    class ClassNotFound(Exception):
        pass

    class InvalidArguments(Exception):
        pass

    def __init__(self, python_ast_indexer: PythonIndexer):
        """
        Initialize the PythonWriter with a PythonIndexer instance.
        """
        self.indexer = python_ast_indexer

    def update_module(self, source_code: str, extending_module: bool = True, **kwargs) -> None:
        """
        Perform an in-place extention or reduction of a module object according to the received code.

        Args:
            source_code (str): The source_code containing the updates or deletions.
            extending_module (bool): True for adding/updating, False for reducing/deleting.
            module_obj (Optional[Module], keyword): The module object to be updated.
            module_path (Optional[str], keyword): The path of the module to be updated.
            class_name (Optional[str], keyword): The name of the class where the update should be applied, will default to modul.
            write_to_disk (Optional[bool], keyword): Writes the changed module to disk.

        Raises:
            InvalidArguments: If both module_obj and module_path are provided or none of them.

        Returns:
            Module: The updated module object.
        """
        module_obj = kwargs.get("module_obj")
        module_path = kwargs.get("module_path")
        class_name = kwargs.get("class_name") or ""

        write_to_disk = kwargs.get("write_to_disk") or False
        self._validate_args(module_obj, module_path, write_to_disk)
        source_code = PythonWriter._clean_input_code(source_code)
        if not module_obj and module_path:
            if module_path not in self.indexer.module_dict:
                self._create_module_from_source_code(module_path, source_code)
            module_obj = self.indexer.module_dict[module_path]
        elif module_obj and (not module_path):
            module_path = self.indexer.get_module_path(module_obj)
            assert module_path != PythonIndexer.NO_RESULT_FOUND_STR
        module_path = cast(str, module_path)
        module_obj = cast(Module, module_obj)
        PythonWriter._update_module(
            source_code,
            module_path,
            module_obj,
            extending_module,
            class_name,
        )
        if write_to_disk:
            self.write_module(module_path)

    def write_module(self, module_path: str) -> None:
        """
        Write the modified AST module to a file at the specified output path.

        Args:
            module_path (str): The file path where the modified module should be written.
        """
        if module_path not in self.indexer.module_dict:
            raise PythonWriter.ModuleNotFound(
                f"Module not found in module dictionary: {module_path}"
            )
        module_obj = self.indexer.module_dict[module_path]
        source_code = ast.unparse(module_obj)
        module_os_rel_path = module_path.replace(self.indexer.PATH_SEP, os.path.sep)
        module_os_abs_path = os.path.join(self.indexer.abs_path, module_os_rel_path)
        os.makedirs(os.path.dirname(module_os_abs_path), exist_ok=True)
        file_path = f"{module_os_abs_path}.py"
        with open(file_path, "w") as output_file:
            output_file.write(source_code)
        subprocess.run(["black", file_path])
        subprocess.run(["isort", file_path])

    def _create_module_from_source_code(self, module_path: str, source_code: str) -> Module:
        """
        Create a Python module from the given source code string.

        Args:
            module_path (str): The path where the new module will be created.
        """
        parsed = ast.parse(source_code, type_comments=True)
        if not isinstance(parsed, Module):
            raise ValueError("The source code does not define a module.")
        self.indexer.module_dict[module_path] = parsed
        return parsed

    @staticmethod
    def _validate_args(
        module_obj: Optional[Module], module_path: Optional[str], write_to_disk: bool
    ) -> None:
        if not (module_obj or module_path) or (module_obj and module_path):
            raise PythonWriter.InvalidArguments(
                "Provide either 'module_obj' or 'module_path', not both or none."
            )
        if not module_path and write_to_disk:
            raise PythonWriter.InvalidArguments(
                "Provide 'module_path' to write the module to disk."
            )

    @staticmethod
    def _update_module(
        source_code: str,
        module_path: str,
        existing_module_obj: Module,
        extending_module: bool,
        class_name: str = "",
    ) -> None:
        """
        Update a module object according to the received code.

        Args:
            source_code (str): The code containing the updates.
            module_path (str): The relative path to the module.
            existing_module_obj Module: The module object to be updated.
            extending_module (bool): If True, add or update the code; if False, remove the code.
        """
        if class_name != "":
            existing_class = PythonWriter._find_function_class_or_method(
                existing_module_obj, class_name
            )
            if not existing_class:
                raise PythonWriter.ClassNotFound(
                    f"Class {class_name} not found in module {module_path}"
                )
            if not isinstance(existing_class, ClassDef):
                raise PythonWriter.ClassNotFound(
                    f"Object {class_name} in module {module_path} is not a class."
                )
            PythonWriter._update_class(
                source_code, cast(ClassDef, existing_class), extending_module
            )
        else:
            new_ast = ast.parse(source_code, type_comments=True)
            for new_node in new_ast.body:
                if isinstance(
                    new_node, (Import, ImportFrom)
                ):  # Check if the node is an import statement
                    PythonWriter._manage_imports(
                        existing_module_obj, new_node, "add" if extending_module else "remove"
                    )  # Handle the import statement

                if isinstance(new_node, (ClassDef, FunctionDef)):
                    obj_name = new_node.name
                    existing_obj = PythonWriter._find_function_class_or_method(
                        existing_module_obj, obj_name
                    )
                    if extending_module:
                        if existing_obj:
                            PythonWriter._update_existing_node(
                                existing_module_obj, new_node, existing_obj
                            )
                        else:
                            PythonWriter._add_ast_node(existing_module_obj, new_node)
                    elif existing_obj:
                        PythonWriter._remove_existing_node(existing_module_obj, existing_obj)

    @staticmethod
    def _update_class(
        source_code: str, existing_class_obj: ClassDef, extending_module: bool
    ) -> None:
        new_ast = ast.parse(source_code, type_comments=True)
        for new_node in new_ast.body:
            if isinstance(new_node, FunctionDef):
                method_name = new_node.name
                existing_method = PythonWriter._find_function_class_or_method(
                    existing_class_obj, method_name
                )
                if extending_module:
                    if existing_method:
                        PythonWriter._update_existing_node(
                            existing_class_obj, new_node, existing_method
                        )
                    else:
                        PythonWriter._add_ast_node(existing_class_obj, new_node)
                elif existing_method:
                    PythonWriter._remove_existing_node(existing_class_obj, existing_method)

    @staticmethod
    def _update_existing_node(
        python_obj: Union[Module, ClassDef],
        new_node: Union[ClassDef, FunctionDef],
        existing_node: Union[ClassDef, FunctionDef],
    ) -> None:
        """
        Update an existing object (class or function) in the module.

        Args:
            module_obj (Module): The module or class object to be updated.
            new_node (Union[ClassDef, FunctionDef]): The new AST node.
            existing_node (Union[ClassDef, FunctionDef]): The existing AST node.
        """
        if isinstance(new_node, ClassDef) and isinstance(existing_node, ClassDef):
            for node in new_node.body:
                class_name = new_node.name
                if isinstance(node, FunctionDef):
                    method_name = node.name
                    lookup_path = f"{class_name}.{method_name}"
                    existing_method = PythonWriter._find_function_class_or_method(
                        python_obj, lookup_path
                    )
                    if existing_method:
                        existing_method.body = node.body
                    else:
                        PythonWriter._add_ast_node(python_obj, node, target_node=existing_node)
        elif isinstance(new_node, FunctionDef) and isinstance(existing_node, FunctionDef):
            existing_node.args = new_node.args
            existing_node.body = new_node.body

    @staticmethod
    def _remove_existing_node(
        python_obj: Union[Module, ClassDef], existing_obj: Union[ClassDef, FunctionDef]
    ) -> None:
        """
        Remove an existing object (class or function) from the module.

        Args:
            python_obj (Union[Module, ClassDef]): The python object to be updated.
            existing_obj (Union[ClassDef, FunctionDef]): The existing AST node.
        """
        if existing_obj in python_obj.body:
            python_obj.body.remove(existing_obj)
        elif isinstance(existing_obj, ClassDef):
            for method_node in existing_obj.body:
                if isinstance(method_node, FunctionDef):
                    if method_node in existing_obj.body:
                        existing_obj.body.remove(method_node)

    @staticmethod
    def _add_ast_node(
        python_obj: Union[Module, ClassDef],
        node: Union[FunctionDef, ClassDef],
        target_node: Optional[Union[ClassDef, Module]] = None,
    ):
        """
        Add an AST node (function or class) to the target node (class or module) in the specified module.

        Args:
            python_obj (Union[Module, ClassDef]): The python object to be updated.
            node (Union[FunctionDef, ClassDef]): The new function or class to add.
            target_node (Optional[Union[ClassDef, Module]]): The target node (class or module) where the new node will be added.
                                                       If not provided, the new node will be added to the module level.
        """
        if target_node is None:
            target_node = python_obj
        target_node.body.append(node)

    @staticmethod
    def _find_function_class_or_method(
        code_obj: Union[Module, ClassDef], lookup_name: str
    ) -> Optional[Union[FunctionDef, ClassDef]]:
        """
        Find a function or method node in a module or class.

        Args:
            module_path (str): The path of the module where the function is located.
            function_name (str): The name of the function to find.
            class_name (Optional[str], optional): The name of the class where the method is located. If not provided, the function is assumed to be at the module level.

        Returns:
            Optional[FunctionDef]: The found function or method node, or None if not found.
        """
        lookup_split = lookup_name.split(".")
        lookup_name = lookup_split[0]
        for node in code_obj.body:
            if isinstance(node, FunctionDef) and node.name == lookup_name:
                assert len(lookup_split) == 1, "Function name is not unique"
                return node
            elif isinstance(node, ClassDef) and node.name == lookup_name:
                if len(lookup_split) == 1:
                    return node
                else:
                    return PythonWriter._find_function_class_or_method(
                        node, ".".join(lookup_split[1:])
                    )
        return None

    @staticmethod
    def _clean_input_code(source_code: str) -> str:
        """
        Take the input source code and remove formatting issues that will cause the AST to fail.

        Args:
            source_code (str): The source code to clean.

        Returns:
            str: The cleaned source code.
        """

        def replace_newline_chars(input_str: str) -> str:
            def replace(match):
                text = match.group(0)
                if text[0] == '"' and text[-1] == '"':
                    return text
                return text.replace("\\n", "\n")

            pattern = "(?x)\n                '.*?'\n                |\n                \".*?\"\n                |\n                [^'\"]+\n            "
            output_str = (
                "".join(
                    (
                        replace(match)
                        for match in re.finditer(
                            pattern,
                            input_str.replace('"""', "ZZ_^^_ZZ").replace("'''", "QQ_^^_QQ"),
                        )
                    )
                )
                .replace("ZZ_^^_ZZ", '"""')
                .replace("QQ_^^_QQ", "'''")
            )
            return output_str

        source_code = replace_newline_chars(source_code)
        source_code = re.sub('\\\\\\"', '"', source_code)
        source_code = source_code.strip()
        return source_code

    @staticmethod
    def _manage_imports(
        module_obj: Module, import_statement: Union[Import, ImportFrom], action: str
    ) -> None:
        if action not in ["add", "remove", "modify"]:
            raise ValueError("Invalid action. Supported actions: 'add', 'remove', 'modify'")

        if not isinstance(import_statement, (Import, ImportFrom)):
            raise ValueError("The provided import statement is not valid.")

        existing_import_node = None
        for node in module_obj.body:
            if isinstance(node, (Import, ImportFrom)):
                if PythonWriter._compare_import_nodes(node, import_statement):
                    existing_import_node = node
                    break

        if action == "add":
            if not existing_import_node:
                module_obj.body.insert(0, import_statement)
        elif action == "remove":
            if existing_import_node:
                module_obj.body.remove(existing_import_node)
        elif action == "modify":
            if existing_import_node:
                module_obj.body.remove(existing_import_node)
                module_obj.body.insert(0, import_statement)

    @staticmethod
    def _compare_import_nodes(
        node1: Union[Import, ImportFrom], node2: Union[Import, ImportFrom]
    ) -> bool:
        if type(node1) != type(node2):
            return False

        if isinstance(node1, Import):
            return node1.names[0].name == node2.names[0].name
        elif isinstance(node1, ImportFrom):
            node1 = cast(ImportFrom, node1)
            node2 = cast(ImportFrom, node2)
            return node1.module == node2.module and node1.names == node2.names

        return False
