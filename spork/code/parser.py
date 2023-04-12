"""
CodeParser

This module provides functionality to extract information about classes, functions,
and their docstrings from a given directory of Python files. It defines the `CodeParser`
class that can be used to lookup the source code, docstrings, and list of functions
or classes within a specific file.

Example usage:
    code_lookup = CodeParser(os.path.join(home_path(), "spork"))

    print("Docstring of a class or function:")
    print(code_lookup.lookup_docstring('ClassNameOrFunctionName'))

    print("Source code of a class or function:")
    print(code_lookup.lookup_code('ClassNameOrFunctionName'))

    print("Standalone functions in a file:")
    print(code_lookup.get_standalone_functions('file_name.py'))

    print("Classes in a file")
    print(code_lookup.get_classes('file_name.py'))

    print("Docstring of a file:")
    print(code_lookup.lookup_file_docstring('file_name.py'))
"""
import ast
import os
from typing import Dict, List, Optional, cast

from ..utils import home_path


class ObjectInfo:
    """
    The ObjectInfo class represents a single object (class or function) with its name, docstring, and raw code.

    Attributes:
        name (str): The name of the object.
        docstring (str): The docstring of the object.
        code (str): The raw code of the object.
    """

    def __init__(self, name: str, docstring: str, code: str):
        self.name = name
        self.docstring = docstring
        self.code = code

    def get_raw_code(self) -> str:
        """
        Returns the raw code of the object.

        Returns:
            str: The raw code of the object as a string.
        """
        return self.code

    def get_doc_string(self) -> str:
        """
        Returns the docstring of the object.

        Returns:
            str: The docstring of the object as a string.
        """
        return self.docstring


class FileObject:
    """
    The FileObject class represents a single file with its filepath, docstring, standalone functions, and classes.

    Attributes:
        filepath (str): The filepath of the file.
        docstring (str): The docstring of the file.
        standalone_functions (List[ObjectInfo]): A list of ObjectInfo instances representing standalone functions.
        classes (List[ObjectInfo]): A list of ObjectInfo instances representing classes.
    """

    def __init__(
        self,
        filepath: str,
        docstring: str,
        standalone_functions: List[ObjectInfo],
        classes: List[ObjectInfo],
    ):
        self.filepath = filepath
        self.docstring = docstring
        self.standalone_functions = standalone_functions
        self.classes = classes

    def get_standalone_functions(self) -> List[ObjectInfo]:
        """
        Returns the list of standalone functions in the file as ObjectInfo instances.

        Returns:
            List[ObjectInfo]: A list of ObjectInfo instances representing the standalone functions in the file.
        """
        return self.standalone_functions

    def get_classes(self) -> List[ObjectInfo]:
        """
        Returns the list of classes in the file as ObjectInfo instances.

        Returns:
            List[ObjectInfo]: A list of ObjectInfo instances representing the classes in the file.
        """
        return self.classes

    def get_docstring(self) -> str:
        """
        Returns the docstring of the file.

        Returns:
            str: The docstring of the file as a string.
        """
        return self.docstring

    def get_summary(self) -> str:
        """
        Returns a formatted summary of the file, including its docstring, classes, class functions, and standalone functions.

        Returns:
            str: A formatted summary of the file as a string.
        """
        summary = [f"File: {self.filepath}", f"Docstring: {self.docstring}\n"]

        summary.append("Standalone Functions:")
        for func in self.standalone_functions:
            summary.append(self.format_standalone_function_summary(func))

        summary.append("\nClasses:")
        for cls in self.classes:
            summary.append(self.format_class_summary(cls))

        return "\n".join(summary)

    @staticmethod
    def format_standalone_function_summary(function: ObjectInfo) -> str:
        """
        Formats the summary of a standalone function.

        Args:
            function (ObjectInfo): The ObjectInfo instance representing the standalone function.

        Returns:
            str: A formatted summary of the standalone function as a string.
        """
        return f"Function: {function.name}\nDocstring: {function.docstring}\n"

    @staticmethod
    def format_class_summary(class_obj: ObjectInfo) -> str:
        """
        Formats the summary of a class, including its class functions.

        Args:
            class_obj (ObjectInfo): The ObjectInfo instance representing the class.

        Returns:
            str: A formatted summary of the class and its functions as a string.
        """
        class_summary = [f"Class: {class_obj.name}", f"Docstring: {class_obj.docstring}\n"]

        # Assuming class_obj.code is an ast.ClassDef node
        class_node = cast(ast.ClassDef, ast.parse(class_obj.code).body[0])

        class_summary.append("Class Functions:")
        for n in class_node.body:
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
                func_name = n.name
                func_docstring = ast.get_docstring(n)
                class_summary.append(f"  Function: {func_name}\n  Docstring: {func_docstring}\n")

        return "\n".join(class_summary)


class CodeParser:
    """
    The CodeParser class provides functionality to extract and access information about
    classes, functions, and their docstrings from a given directory of Python files.

    Attributes:
        file_dict (Dict[str, FileObject]): A dictionary that maps file names to their corresponding FileObject instances.
    """

    def __init__(self, root_dir: Optional[str] = None):
        self.file_dict: Dict[str, FileObject] = {}
        self._populate_file_dict(root_dir if root_dir else os.path.join(home_path(), "spork"))

    def lookup_code(self, object_name: str) -> str:
        """
        Returns the raw code of an function or class with the given name, or None if the object is not found.

        Args:
            object_name (str): The name of the object (class or function) to look up.

        Returns:
            Optional[str]: The raw code of the object, or None if the object is not found.
        """
        for file_obj in self.file_dict.values():
            for obj in file_obj.get_standalone_functions() + file_obj.get_classes():
                if obj.name == object_name:
                    return obj.get_raw_code()
        return "No result found"

    def lookup_docstring(self, object_name: str) -> Optional[str]:
        """
        Returns the docstring of the object with the given name, or None if the object is not found.

        Args:
            object_name (str): The name of the object (class or function) to look up.

        Returns:
            Optional[str]: The docstring of the object, or None if the object is not found.
        """
        for file_obj in self.file_dict.values():
            for obj in file_obj.get_standalone_functions() + file_obj.get_classes():
                if obj.name == object_name:
                    return obj.get_doc_string()
        return "No result found"

    def get_standalone_functions(self, file_name: str) -> List[str]:
        """
        Returns the list of standalone function names in the given file, or None if the file is not found.

        Args:
            file_name (str): The name of the file to look up.

        Returns:
            Optional[List[str]]: A list of standalone function names found in the file, or None if the file is not found.
        """
        if file_name in self.file_dict:
            return [func.name for func in self.file_dict[file_name].get_standalone_functions()]
        return ["No results found."]

    def get_classes(self, file_name: str) -> List[str]:
        """
        Returns the list of class names in a file, or None if the file is not found.

        Args:
            file_name (str): The name of the file.

        Returns:
            Optional[List[str]]: A list of class names found in the file, or None if the file is not found.
        """
        if file_name in self.file_dict:
            return [cls.name for cls in self.file_dict[file_name].get_classes()]
        return ["No results found."]

    def lookup_file_docstring(self, file_name: str) -> str:
        """
        Returns the docstring of a file, or None if the file is not found.

        Args:
            file_name (str): The name of the file.

        Returns:
            Optional[str]: The docstring of the file, or None if the file is not found.
        """
        if file_name in self.file_dict:
            return self.file_dict[file_name].get_docstring()
        return "No results found."

    def build_file_summary(self, file_name: str) -> str:
        """
        Returns a formatted summary of the specified file, or None if the file is not found.

        Args:
            file_name (str): The name of the file.

        Returns:
            Optional[str]: A formatted summary of the file, or None if the file is not found.
        """
        if file_name in self.file_dict:
            return self.file_dict[file_name].get_summary()
        return "No results found."

    def _populate_file_dict(self, root_dir: str) -> None:
        """
        Populates the file_dict with FileObjects for each Python file found in the specified directory.

        Args:
            root_dir (str): The root directory containing the Python files.
        """
        for root, _dirs, files in os.walk(root_dir):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
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
                            function = ObjectInfo(
                                func_name, func_docstring if func_docstring else "", func_code
                            )
                            standalone_functions.append(function)
                        elif isinstance(n, ast.ClassDef):
                            class_name = n.name
                            class_docstring = ast.get_docstring(n)
                            class_code = "".join(ast.unparse(n))
                            class_obj = ObjectInfo(
                                class_name, class_docstring if class_docstring else "", class_code
                            )
                            classes.append(class_obj)

                    self.file_dict[file] = FileObject(
                        file_path, docstring if docstring else "", standalone_functions, classes
                    )


if __name__ == "__main__":
    print("Performing code lookup")
    code_parser = CodeParser(os.path.join(home_path(), "spork"))
    print("Done loading the Code Parser")
    print("Login Github:\n%s" % (code_parser.lookup_code("login_github")))
    print("Lookup Docstring:\n%s" % (code_parser.lookup_docstring("login_github")))
    print("Get StandAlone Functions:\n%s" % (code_parser.get_standalone_functions("utils.py")))
    print("Get Classes:\n%s" % (code_parser.get_classes("utils.py")))
    print("Lookup File DocString:\n%s" % (code_parser.lookup_file_docstring("utils.py")))
    print("Lookup File Summary:\n%s" % (code_parser.build_file_summary("parser.py")))
