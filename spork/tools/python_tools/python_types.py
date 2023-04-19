"""
PythonObjectTypes

There are several major PythonObjectType subclasses:
    - PythonFunctionType
    - PythonClassType
    - PythonModuleType
    - PythonPackageType
These classes are used to represent Python objects in the PythonTools class.
"""
import abc
import ast
from typing import Any, Callable, Dict, List, Tuple, cast

RESULT_NOT_FOUND = "No results found."


class PythonObjectType(abc.ABC):
    """
    The PythonObjectType class represents a single object with its python path, docstring, and raw code.

    Attributes:
        py_path (str): The name of the object.
        docstring (str): The docstring of the object.
        code (str): The raw code of the object.
    """

    def __init__(self, py_path: str, docstring: str, code: str):
        self.py_path = py_path
        self.docstring = docstring
        self.code = code

    def get_raw_code(self):
        pass

    def get_docstring(self):
        pass

    def update_code(
        self, new_code: str, notify_update: Callable[[str, str, Dict[str, Any]], None]
    ):
        pass

    @classmethod
    def from_code(cls, py_path: str, code: str, _imports: List[str]):
        pass


class PythonFunctionType(PythonObjectType):
    """
    The PythonFunctionType class represents a single function (or method) with its python path, docstring, and raw code.

    Attributes:
        methods (Dict[str, PythonFunctionType]): A dictionary of associated PythonFunctionType instances, keyed by method names.
    """

    def __init__(self, py_path: str, docstring: str, code: str):
        super().__init__(py_path, docstring, code)

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
            if isinstance(node.body[0].body[0], ast.Expr) and isinstance(
                node.body[0].body[0].value, ast.Str
            ):
                node.body[0].body.pop(0)
        return ast.unparse(node)

    def get_docstring(self) -> str:
        """
        Returns the docstring of the object.

        Note:
            This method may be extended by subclasses to customize the behavior.

        Returns:
            str: The docstring of the object as a string.
        """
        name = self.py_path.split(".")[-1]
        return f"{name}:\n{self.docstring}" if self.docstring else RESULT_NOT_FOUND

    def update_code(
        self, new_code: str, notify_update: Callable[[str, str, Dict[str, Any]], None]
    ) -> None:
        """
        Updates the raw code and the docstring of the PythonFunctionType instance.

        Args:
            new_code (str): The new raw code to replace the existing code.
            notify_update (Callable[[str, str, Dict[str, Any]], None]): A callback function that is called when the code is updated.
                The function should take two arguments: an entity type (e.g., "function") and the python path.

        Returns:
            None
        """
        self.code = new_code
        notify_update("function", self.py_path, {})
        node = ast.parse(new_code)
        if isinstance(node.body[0], (ast.FunctionDef, ast.AsyncFunctionDef)):
            self.docstring = ast.get_docstring(node.body[0]) or RESULT_NOT_FOUND

    @classmethod
    def from_code(cls, py_path: str, code: str, _imports: List[str] = []) -> "PythonFunctionType":
        """
        Creates a PythonFunctionType instance from an AST node.

        Args:
            node (ast.AST): The AST node representing the Python object.
            py_path (str): The Python path of the object.

        Returns:
            PythonFunctionType: A new PythonFunctionType instance.
        """
        tree = ast.parse(code)
        # Access the ClassDef node inside the Module node's body
        function_node = cast(ast.FunctionDef, tree.body[0])
        docstring = ast.get_docstring(function_node) or RESULT_NOT_FOUND

        return cls(py_path, docstring, code)


class PythonClassType(PythonObjectType):
    """
    The PythonClassType class represents a single class with its python path, docstring, and raw code.

    Attributes:
        py_path (str): The name of the class.
        docstring (str): The docstring of the class.
        code (str): The raw code of the class.
        methods (Dict[str, PythonFunctionType]): A dictionary of associated PythonFunctionType instances, keyed by method names.
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

    def get_docstring(self, exclude_methods: bool = False) -> str:
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
                result += f"\n{method.get_docstring()}"

        return result

    def update_code(
        self, new_code: str, notify_update: Callable[[str, str, Dict[str, Any]], None]
    ) -> None:
        """
        Updates the raw code and the docstring of the PythonFunctionType instance.

        Args:
            new_code (str): The new raw code to replace the existing code.
            notify_update (Callable[[str, str, Dict[str, Any]], None]): A callback function that is called when the code is updated.
                The function should take two arguments: an entity type (e.g., "function") and the python path.

        Returns:
            None
        """
        self.code = new_code
        node = ast.parse(new_code)
        if isinstance(node.body[0], ast.ClassDef):
            class_node = node.body[0]
            self.docstring = ast.get_docstring(class_node) or RESULT_NOT_FOUND
            self.code = new_code
            self.methods = self._parse_methods()
        notify_update("class", self.py_path, {})

    @classmethod
    def from_code(cls, py_path: str, code: str, _imports: List[str] = []) -> "PythonClassType":
        """
        Creates a PythonModuleType instance from an AST node.

        Args:
            node (ast.AST): The AST node representing the Python module.
            py_path (str): The Python path of the module.

        Returns:
            PythonModuleType: A new PythonModuleType instance.
        """
        tree = ast.parse(code)
        class_node = None
        for node in ast.iter_child_nodes(tree):
            if isinstance(node, ast.ClassDef):
                class_node = node
                break
        # Get the class docstring
        class_docstring = RESULT_NOT_FOUND
        if class_node:
            for stmt in class_node.body:
                if isinstance(stmt, ast.Expr) and (
                    isinstance(stmt.value, (ast.Str, ast.Constant))
                    and isinstance(stmt.value.value, str)
                ):
                    class_docstring = stmt.value.value
                    break
            else:
                class_docstring = RESULT_NOT_FOUND
        return cls(py_path, class_docstring, code)

    def _parse_methods(self) -> Dict[str, PythonFunctionType]:
        """
        Parses the code and extracts its methods as PythonFunctionType instances.

        Returns:
            Dict[str, PythonFunctionType]: A dictionary of associated PythonFunctionType instances, keyed by method names.
        """
        parsed_code = ast.parse(self.code)
        class_node = None

        # Search for the class definition within the parsed code
        for node in parsed_code.body:
            if isinstance(node, ast.ClassDef):
                class_node = node
                break

        if class_node is None:
            raise ValueError("No class definition found in the provided code")

        methods = {}

        for n in class_node.body:
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
                func_name = n.name
                func_docstring = ast.get_docstring(n) or RESULT_NOT_FOUND
                func_code = ast.unparse(n)
                methods[f"{self.py_path}.{func_name}"] = PythonFunctionType(
                    f"{self.py_path}.{func_name}", func_docstring, func_code
                )
        return methods


class PythonModuleType(PythonObjectType):
    """
    The PythonModuleType class represents a single python module with associated docstrings, standalone functions, and classes.

    Attributes:
        filepath (str): The filepath of the file.
        docstring (str): The docstring of the file.
        standalone_functions (Dict[str, PythonFunctionType]): A list of PythonFunctionType instances representing standalone functions.
        classes (List[PythonFunctionType]): A list of PythonFunctionType instances representing classes.
    """

    def __init__(
        self,
        py_path: str,
        docstring: str,
        standalone_functions: Dict[str, PythonFunctionType],
        classes: Dict[str, PythonClassType],
        imports: List[str],
    ):
        super().__init__(py_path, docstring, RESULT_NOT_FOUND)
        self.standalone_functions = standalone_functions
        self.classes = classes
        self.imports = imports

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
            for func_obj in self.standalone_functions.values():
                raw_code.append(func_obj.get_raw_code())
                raw_code.append("\n")

        for class_obj in self.classes.values():
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
            for func_obj in self.standalone_functions.values():
                docstrings.append(func_obj.get_docstring())
                docstrings.append("\n")

        for class_obj in self.classes.values():
            docstrings.append(class_obj.get_docstring(exclude_methods))
            docstrings.append("\n")

        return "\n".join(docstrings) if len(docstrings) > 0 else RESULT_NOT_FOUND

    def update_code(
        self, new_code: str, notify_update: Callable[[str, str, Dict[str, Any]], None]
    ) -> None:
        """
        Updates the raw code and the docstring of the PythonFunctionType instance.

        Args:
            new_code (str): The new raw code to replace the existing code.
            notify_update (Callable[[str, str, Dict[str, Any]], None]): A callback function that is called when the code is updated.
                The function should take two arguments: an entity type (e.g., "function") and the python path.

        Returns:
            None
        """
        self.code = new_code
        notify_update("module", self.py_path, {})
        node = ast.parse(new_code)
        self.docstring = ast.get_docstring(node) or RESULT_NOT_FOUND
        self.standalone_functions, self.classes = self._parse_functions_and_classes(
            self.py_path, node
        )

    @classmethod
    def from_code(cls, py_path: str, code: str, imports: List[str]) -> "PythonModuleType":
        """
        Creates a PythonModuleType instance from an AST node.

        Args:
            node (ast.AST): The AST node representing the Python class.
            py_path (str): The Python path of the class.

        Returns:
            PythonModuleType: A new PythonModuleType instance.
        """
        tree = ast.parse(code)
        docstring = ast.get_docstring(tree) or RESULT_NOT_FOUND
        standalone_functions, classes = cls._parse_functions_and_classes(py_path, tree)
        return cls(py_path, docstring, standalone_functions, classes, imports)

    @staticmethod
    def _parse_functions_and_classes(
        py_path: str,
        node: ast.Module,
    ) -> Tuple[Dict[str, PythonFunctionType], Dict[str, PythonClassType]]:
        standalone_functions = {}
        classes = {}

        for n in node.body:
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
                func_name = n.name
                func_docstring = ast.get_docstring(n) or RESULT_NOT_FOUND
                func_code = ast.unparse(n)
                standalone_functions[f"{py_path}.{func_name}"] = PythonFunctionType(
                    f"{py_path}.{func_name}", func_docstring, func_code
                )
            elif isinstance(n, ast.ClassDef):
                class_name = n.name
                class_docstring = ast.get_docstring(n) or RESULT_NOT_FOUND
                class_code = ast.unparse(n)
                class_obj = PythonClassType(f"{py_path}.{class_name}", class_docstring, class_code)
                classes[f"{py_path}.{class_name}"] = class_obj

        return standalone_functions, classes


class PythonPackageType(PythonObjectType):
    def __init__(self, py_path: str, modules: Dict[str, PythonModuleType]):
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

    def update_code(
        self, new_code: str, notify_update: Callable[[str, str, Dict[str, Any]], None]
    ):
        # Not applicable for PythonPackageType as it doesn't hold any code directly.
        pass

    # TODO - Consider how to implement this.
    @classmethod
    def from_code(cls, py_path: str, code: str, _imports: List[str] = []):
        pass
