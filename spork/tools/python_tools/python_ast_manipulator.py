"""
PythonASTManipulator - A utility class for manipulating with Python AST nodes.

This class provides methods for creating AST nodes from source code strings, and updating existing module objects with new code.
It also allows for extending and reducing module functionality by adding, updating or removing classes, methods, and functions.

Example usage:

    ast_wrapper = PythonASTManipulator()

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
from ast import ClassDef, FunctionDef, Module
from typing import Dict, Optional, Union


class PythonASTManipulator:
    """
    A utility class for working with Python AST nodes.

    Public Methods:

        update_module(
            code: str,
            extending_module: bool,
            module_obj (Optional[Module], keyword),
            module_path (Optional[str], keyword)
        ) -> None:
            Perform an in-place extention or reduction of a module object according to the received code.

        Exceptions:
            ModuleNotFound: Raised when a module cannot be found.
            InvalidArguments: Raised when invalid arguments are passed to a method.
    """

    class ModuleNotFound(Exception):
        pass

    class InvalidArguments(Exception):
        pass

    def __init__(self):
        self.module_dict: Dict[str, Module] = {}
        pass

    def update_module(
        self,
        code: str,
        extending_module: bool = True,
        **kwargs,
    ) -> None:
        """
        Perform an in-place extention or reduction of a module object according to the received code.

        Args:
            code (str): The code containing the updates or deletions.
            extending_module (bool): True for adding/updating, False for reducing/deleting.
            module_obj (Optional[Module], keyword): The module object to be updated.
            module_path (Optional[str], keyword): The path of the module to be updated.

        Raises:
            ModuleNotFound: If the module is not found in the module dictionary.
            InvalidArguments: If both module_obj and module_path are provided or none of them.

        Returns:
            Module: The updated module object.
        """
        module_obj = kwargs.get("module_obj")
        module_path = kwargs.get("module_path")

        self._validate_args(module_obj, module_path)

        if not module_obj:
            if module_path not in self.module_dict:
                raise PythonASTManipulator.ModuleNotFound(
                    f"Module not found in module dictionary: {module_path}"
                )

            module_obj = self.module_dict[module_path]

        PythonASTManipulator._update_module(code, module_obj, extending_module)

    @staticmethod
    def _validate_args(module_obj: Optional[Module], module_path: Optional[str]) -> None:
        if not (module_obj or module_path) or (module_obj and module_path):
            raise PythonASTManipulator.InvalidArguments(
                "Provide either 'module_obj' or 'module_path', not both or none."
            )

    @staticmethod
    def _update_module(
        code: str,
        module_obj: Module,
        extending_module: bool,
    ) -> None:
        """
        Update a module object according to the received code.

        Args:
            code (str): The code containing the updates.
            module_obj Module: The module object to be updated.
            extending_module (bool): If True, add or update the code; if False, remove the code.
        """

        new_ast = ast.parse(code)
        for new_node in new_ast.body:
            if isinstance(new_node, (ast.ClassDef, ast.FunctionDef)):
                obj_name = new_node.name
                existing_obj = PythonASTManipulator._find_class_or_function(module_obj, obj_name)

                if extending_module:
                    if existing_obj:
                        PythonASTManipulator._update_existing_object(
                            module_obj, new_node, existing_obj
                        )
                    else:
                        PythonASTManipulator._add_ast_node(module_obj, new_node)
                else:
                    if existing_obj:
                        PythonASTManipulator._remove_existing_object(module_obj, existing_obj)

    @staticmethod
    def _update_existing_object(
        module_obj: Module,
        new_node: Union[ast.ClassDef, ast.FunctionDef],
        existing_obj: Union[ast.ClassDef, ast.FunctionDef],
    ) -> None:
        """
        Update an existing object (class or function) in the module.

        Args:
            module_obj (Module): The module object to be updated.
            new_node (Union[ast.ClassDef, ast.FunctionDef]): The new AST node.
            existing_obj (Union[ast.ClassDef, ast.FunctionDef]): The existing AST node.
        """
        if isinstance(new_node, ast.ClassDef) and isinstance(existing_obj, ast.ClassDef):
            for class_node in new_node.body:
                if isinstance(class_node, ast.FunctionDef):
                    method_name = class_node.name
                    existing_method = PythonASTManipulator._find_class_or_function(
                        module_obj, method_name
                    )

                    if existing_method:
                        existing_method.args = class_node.args
                        existing_method.body = class_node.body
                    else:
                        PythonASTManipulator._add_ast_node(
                            module_obj, class_node, target_node=existing_obj
                        )
        elif isinstance(new_node, ast.FunctionDef) and isinstance(existing_obj, ast.FunctionDef):
            existing_obj.args = new_node.args
            existing_obj.body = new_node.body

    @staticmethod
    def _remove_existing_object(
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
    def _create_module_from_source(source: str) -> Module:
        """
        Create a Python module from the given source code string.

        Args:
            module_path (str): The path where the new module will be created.
        """
        parsed = ast.parse(source)
        if not isinstance(parsed, ast.Module):
            raise ValueError("The source code does not define a module.")
        return parsed

    @staticmethod
    def _create_function_from_source(source: str) -> ast.FunctionDef:
        """
        Create a Python function from the given source code string.

        Args:
            source (str): The source code string of the function.

        Returns:
            ast.FunctionDef: The created function as an AST node.
        """
        parsed = ast.parse(source)
        function_node = parsed.body[0]
        if not isinstance(function_node, ast.FunctionDef):
            raise ValueError("The source code does not define a function.")
        return function_node

    @staticmethod
    def _create_class_from_source(source: str) -> ast.ClassDef:
        """
        Create a Python class from the given source code string.

        Args:
            source (str): The source code string of the class.

        Returns:
            ast.ClassDef: The created class as an AST node.
        """
        parsed = ast.parse(source)
        class_node = parsed.body[0]
        if not isinstance(class_node, ast.ClassDef):
            raise ValueError("The source code does not define a class.")
        return class_node

    @staticmethod
    def _find_class_or_function(
        code_obj: Union[Module, ClassDef], obj_name: str
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

        # Find the method node in the class
        for node in code_obj.body:
            if isinstance(node, ast.FunctionDef) and node.name == obj_name:
                return node
            elif isinstance(node, ast.ClassDef) and node.name == obj_name:
                return node

        return None
