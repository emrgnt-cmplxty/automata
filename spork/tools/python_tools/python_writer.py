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
import subprocess
from ast import ClassDef, FunctionDef, Module
from typing import Optional, Union

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

    class InvalidArguments(Exception):
        pass

    def __init__(self, python_ast_indexer: PythonIndexer):
        """
        Initialize the PythonWriter with a PythonIndexer instance.
        """
        self.indexer = python_ast_indexer

    def update_module(
        self,
        source_code: str,
        extending_module: bool = True,
        **kwargs,
    ) -> None:
        """
        Perform an in-place extention or reduction of a module object according to the received code.

        Args:
            source_code (str): The source_code containing the updates or deletions.
            extending_module (bool): True for adding/updating, False for reducing/deleting.
            module_obj (Optional[Module], keyword): The module object to be updated.
            module_path (Optional[str], keyword): The path of the module to be updated.
            write_to_disk (Optional[bool], keyword): Writes the changed module to disk.

        Raises:
            InvalidArguments: If both module_obj and module_path are provided or none of them.

        Returns:
            Module: The updated module object.
        """
        module_obj = kwargs.get("module_obj")
        module_path = kwargs.get("module_path")
        write_to_disk = kwargs.get("write_to_disk") or False

        self._validate_args(module_obj, module_path, write_to_disk)

        if not module_obj and module_path:
            if module_path not in self.indexer.module_dict:
                self._create_module_from_source_code(module_path, source_code)
            module_obj = self.indexer.module_dict[module_path]
        elif module_obj and not module_path:
            module_path = self.indexer.get_module_path(module_obj)
            print("module_path = ", module_path)
            assert module_path != PythonIndexer.NO_RESULT_FOUND_STR
        PythonWriter._update_module(source_code, module_path, module_obj, extending_module)  # type: ignore
        print("write_to_disk = ", write_to_disk)
        if write_to_disk:
            print("calling write to disk at path module_path = ", module_path)
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
        # Add path relative to indexer to the output path
        module_os_abs_path = os.path.join(self.indexer.abs_path, module_os_rel_path)
        # Make directories if they do not exist
        os.makedirs(os.path.dirname(module_os_abs_path), exist_ok=True)
        file_path = f"{module_os_abs_path}.py"
        print("module_os_abs_path = ", module_os_abs_path)
        with open(file_path, "w") as output_file:
            print(" source_code = ", source_code)
            output_file.write(source_code)
        subprocess.run(["black", file_path])
        subprocess.run(["isort", file_path])

    def _create_module_from_source_code(self, module_path: str, source_code: str) -> Module:
        """
        Create a Python module from the given source code string.

        Args:
            module_path (str): The path where the new module will be created.
        """
        parsed = ast.parse(source_code)
        if not isinstance(parsed, ast.Module):
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
    ) -> None:
        """
        Update a module object according to the received code.

        Args:
            source_code (str): The code containing the updates.
            module_path (str): The relative path to the module.
            existing_module_obj Module: The module object to be updated.
            extending_module (bool): If True, add or update the code; if False, remove the code.
        """
        print("receiving source code = ", source_code)
        new_ast = ast.parse(source_code)
        for new_node in new_ast.body:
            if isinstance(new_node, (ast.ClassDef, ast.FunctionDef)):
                obj_name = new_node.name
                existing_obj = PythonWriter._find_function_class_or_method(
                    existing_module_obj, obj_name
                )

                if extending_module:
                    if existing_obj:
                        print("in A")
                        PythonWriter._update_existing_node(
                            module_path, existing_module_obj, new_node, existing_obj
                        )
                    else:
                        print("in B")
                        PythonWriter._add_ast_node(existing_module_obj, new_node)
                else:
                    if existing_obj:
                        print("in C")
                        PythonWriter._remove_existing_node(existing_module_obj, existing_obj)

    @staticmethod
    def _update_existing_node(
        module_path: str,
        module_obj: Module,
        new_node: Union[ast.ClassDef, ast.FunctionDef],
        existing_node: Union[ast.ClassDef, ast.FunctionDef],
    ) -> None:
        """
        Update an existing object (class or function) in the module.

        Args:
            module_obj (Module): The module object to be updated.
            new_node (Union[ast.ClassDef, ast.FunctionDef]): The new AST node.
            existing_node (Union[ast.ClassDef, ast.FunctionDef]): The existing AST node.
        """
        if isinstance(new_node, ast.ClassDef) and isinstance(existing_node, ast.ClassDef):
            for node in new_node.body:
                class_name = new_node.name
                if isinstance(node, ast.FunctionDef):
                    method_name = node.name
                    print("class_name = ", class_name)
                    print("method_name = ", method_name)
                    print("module_path = ", module_path)
                    lookup_path = f"{class_name}.{method_name}"
                    print("lookup_path = ", lookup_path)
                    existing_method = PythonWriter._find_function_class_or_method(
                        module_obj, lookup_path
                    )
                    print("existing_method = ", existing_method)

                    if existing_method:
                        existing_method.body = node.body
                    else:
                        PythonWriter._add_ast_node(module_obj, node, target_node=existing_node)
        elif isinstance(new_node, ast.FunctionDef) and isinstance(existing_node, ast.FunctionDef):
            existing_node.args = new_node.args
            existing_node.body = new_node.body

    @staticmethod
    def _remove_existing_node(
        module_obj: Module, existing_obj: Union[ast.ClassDef, ast.FunctionDef]
    ) -> None:
        """
        Remove an existing object (class or function) from the module.

        Args:
            module_obj (Module): The module object to be updated.
            existing_obj (Union[ast.ClassDef, ast.FunctionDef]): The existing AST node.
        """
        if existing_obj in module_obj.body:
            module_obj.body.remove(existing_obj)
        elif isinstance(existing_obj, ast.ClassDef):
            for method_node in existing_obj.body:
                if isinstance(method_node, ast.FunctionDef):
                    if method_node in existing_obj.body:
                        existing_obj.body.remove(method_node)

    @staticmethod
    def _add_ast_node(
        module_obj: Module,
        node: Union[FunctionDef, ClassDef],
        target_node: Optional[Union[ClassDef, Module]] = None,
    ):
        """
        Add an AST node (function or class) to the target node (class or module) in the specified module.

        Args:
            module_path (str): The path of the module where the new node will be added.
            node (Union[FunctionDef, ClassDef]): The new function or class to add.
            target_node (Optional[Union[ClassDef, Module]]): The target node (class or module) where the new node will be added.
                                                       If not provided, the new node will be added to the module level.
        """
        if target_node is None:
            # Add the new node to the module level
            target_node = module_obj

        # Add the new node to the target_node's body
        target_node.body.append(node)

    @staticmethod
    def _find_function_class_or_method(
        code_obj: Union[Module, ClassDef], lookup_name: str
    ) -> Optional[Union[ast.FunctionDef, ast.ClassDef]]:
        """
        Find a function or method node in a module or class.

        Args:
            module_path (str): The path of the module where the function is located.
            function_name (str): The name of the function to find.
            class_name (Optional[str], optional): The name of the class where the method is located. If not provided, the function is assumed to be at the module level.

        Returns:
            Optional[ast.FunctionDef]: The found function or method node, or None if not found.
        """
        lookup_split = lookup_name.split(".")
        lookup_name = lookup_split[0]
        # Find the method node in the class
        for node in code_obj.body:
            print("node = ", node)
            if isinstance(node, ast.FunctionDef) and node.name == lookup_name:
                assert len(lookup_split) == 1, "Function name is not unique"
                return node
            elif isinstance(node, ast.ClassDef) and node.name == lookup_name:
                if len(lookup_split) == 1:
                    return node
                else:
                    return PythonWriter._find_function_class_or_method(
                        node, ".".join(lookup_split[1:])
                    )

        return None
