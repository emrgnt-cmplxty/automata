import os
import ast
from ast import ClassDef, FunctionDef, Module
from typing import Dict, Optional, Union, cast


class PythonASTIndexer:
    NO_RESULT_FOUND_STR = "No Result Found."
    PATH_SEP = "."

    def __init__(self, root_dir):
        self.root_dir = root_dir
        self.module_dict = self._build_module_dict()

    def retrieve_code(self, module_path: str, object_path: Optional[str]) -> Optional[str]:
        if module_path not in self.module_dict:
            return PythonASTIndexer.NO_RESULT_FOUND_STR

        module = self.module_dict[module_path]
        result = self._find_module_class_function_or_method(module, object_path)
        self._remove_docstrings(result)

        return ast.unparse(result)

    def retrieve_docstring(self, module_path: str, object_path: Optional[str]) -> Optional[str]:
        if module_path not in self.module_dict:
            return PythonASTIndexer.NO_RESULT_FOUND_STR

        module = self.module_dict[module_path]
        result = self._find_module_class_function_or_method(module, object_path)
        docstring = ast.get_docstring(result)

        return docstring if docstring else PythonASTIndexer.NO_RESULT_FOUND_STR

    def _build_module_dict(self) -> Dict[str, Module]:
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
    def _load_module_from_path(path) -> Module:
        try:
            module = ast.parse(open(path).read())
            return module
        except Exception as e:
            print(f"Failed to load module '{path}' due to: {e}")
            return None

    @staticmethod
    def _find_module_class_function_or_method(
        code_obj: Union[Module, ClassDef], object_path: Optional[str]
    ) -> Optional[Union[ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef]]:
        """
        Find a module, or find a function, method or class inside a module.

        Args:
            module_path (str): The path of the module where the function is located.
            function_name (str): The name of the function to find.
            class_name (Optional[str], optional): The name of the class where the method is located. If not provided, the function is assumed to be at the module level.

        Returns:
            Optional[ast.FunctionDef]: The found function or method node, or None if not found.
        """
        if object_path is None:
            assert isinstance(code_obj, ast.Module)
            return cast(ast.Module, code_obj)

        obj_parts = object_path.split(PythonASTIndexer.PATH_SEP)

        if len(obj_parts) == 1:
            return PythonASTIndexer._find_node(code_obj, obj_parts[0])
        elif len(obj_parts) == 2:
            class_node = PythonASTIndexer._find_node(code_obj, obj_parts[0])
            if class_node and isinstance(class_node, ast.ClassDef):
                return PythonASTIndexer._find_node(class_node, obj_parts[1])
        return None

    @staticmethod
    def _find_node(
        code_obj: Union[Module, ClassDef], obj_name: str
    ) -> Optional[Union[ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef]]:
        for node in code_obj.body:
            if isinstance(node, ast.FunctionDef) and node.name == obj_name:
                return node
            elif isinstance(node, ast.ClassDef) and node.name == obj_name:
                return node
        return None

    @staticmethod
    def _remove_docstrings(
        result: Union[ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Module]
    ):
        if isinstance(result, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if isinstance(result.body[0], ast.Expr) and isinstance(result.body[0].value, ast.Str):
                result.body.pop(0)

        if isinstance(result, ast.ClassDef):
            for node in result.body:
                PythonASTIndexer._remove_docstrings(node)

        if isinstance(result, ast.Module):
            if isinstance(result.body[0], ast.Expr) and isinstance(result.body[0].value, ast.Str):
                result.body.pop(0)
            for node in result.body:
                PythonASTIndexer._remove_docstrings(node)
