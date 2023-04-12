import abc
import ast
from typing import Dict, List, cast

RESULT_NOT_FOUND = "No results found."


class PythonObject(abc.ABC):
    """
    The PythonObject class represents a single object with its python path, docstring, and raw code.

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


class PythonFunction(PythonObject):
    """
    The PythonFunction class represents a single function (or method) with its python path, docstring, and raw code.

    Attributes:
        methods (Dict[str, PythonFunction]): A dictionary of associated PythonFunction instances, keyed by method names.
    """

    def __init__(self, py_path: str, docstring: str, code: str):
        super().__init__(py_path, docstring, code)


class PythonClass(PythonObject):
    """
    The PythonClass class represents a single class with its python path, docstring, and raw code.

    Attributes:
        py_path (str): The name of the class.
        docstring (str): The docstring of the class.
        code (str): The raw code of the class.
        methods (Dict[str, PythonFunction]): A dictionary of associated PythonFunction instances, keyed by method names.
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

    def _parse_methods(self) -> Dict[str, PythonFunction]:
        """
        Parses the class code and extracts its methods as PythonFunction instances.

        Returns:
            Dict[str, PythonFunction]: A dictionary of associated PythonFunction instances, keyed by method names.
        """
        # Assuming self.code is an ast.ClassDef node
        class_node = cast(ast.ClassDef, ast.parse(self.code).body[0])
        methods = {}

        for n in class_node.body:
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
                func_name = n.name
                func_docstring = ast.get_docstring(n) or RESULT_NOT_FOUND
                func_code = ast.unparse(n)
                methods[func_name] = PythonFunction(func_name, func_docstring, func_code)

        return methods


class PythonModule(PythonObject):
    """
    The PythonModule class represents a single python module with associated docstrings, standalone functions, and classes.

    Attributes:
        filepath (str): The filepath of the file.
        docstring (str): The docstring of the file.
        standalone_functions (List[PythonFunction]): A list of PythonFunction instances representing standalone functions.
        classes (List[PythonFunction]): A list of PythonFunction instances representing classes.
    """

    def __init__(
        self,
        py_path: str,
        docstring: str,
        standalone_functions: List[PythonFunction],
        classes: List[PythonClass],
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


class PythonPackageType(PythonObject):
    def __init__(self, py_path: str, modules: Dict[str, PythonModule]):
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
