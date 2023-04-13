"""
PythonParserToolBuilder

A class for interacting with the PythonParser API, which provides functionality to extract
information about classes, functions, and their docstrings from a given directory of Python files.

The PythonParserToolBuilder class builds a list of Tool PythonObjects, each representing a specific
command to interact with the PythonParser API.

Attributes:
- code_parser (PythonParser): A PythonParser PythonObjectType representing the code parser to work with.
- logger (Optional[PassThroughBuffer]): An optional PassThroughBuffer PythonObjectType to log output.

Example usage:
    code_parser = PythonParser(os.path.join(home_path(), "your_directory"))
    code_parser_tool_builder = PythonParserToolBuilder(code_parser)
    tools = code_parser_tool_builder.build_tools()

"""

from typing import List, Optional

from langchain.agents import Tool

from ..utils import PassThroughBuffer
from .python_parser import PythonParser


class PythonParserToolBuilder:
    def __init__(self, code_parser: PythonParser, logger: Optional[PassThroughBuffer] = None):
        """
        Initializes a PythonParserToolBuilder PythonObjectType with the given inputs.

        Args:
        - code_parser (PythonParser): A PythonParser PythonObjectType representing the code parser to work with.
        - logger (Optional[PassThroughBuffer]): An optional PassThroughBuffer PythonObjectType to log output.

        Returns:
        - None
        """
        self.code_parser = code_parser
        self.logger = logger

    def build_tools(self) -> List[Tool]:
        """
        Builds a list of Tool PythonObjects for interacting with PythonParser.

        Args:
        - None

        Returns:
        - tools (List[Tool]): A list of Tool PythonObjects representing PythonParser commands.
        """
        tools = [
            Tool(
                name="code-parser-get-raw-code",
                func=lambda PythonObject_py_path: self.code_parser.get_raw_code(
                    PythonObject_py_path
                ),
                description=f"Returns the raw code of the python package, module, class, method, or function with the given path,"
                f' or "No results found" if there is no match found.'
                f' For example, if the function "my_function" is defined in the file "my_file.py" '
                f' located in the main working directory, then the input "my_file.my_function" will return the raw code of the function.'
                f' If the file is off the main directory, then the input should be "my_directory.my_file.my_function".'
                f" To save valuable prompt space, package raw code excludes module standalone functions and class methods.",
                return_direct=True,
            ),
            Tool(
                name="code-parser-get-PythonObjectType-docstring",
                func=lambda PythonObject_py_path: self.code_parser.get_docstring(
                    PythonObject_py_path
                ),
                description=f"Identical to code-parser-get-PythonObjectType-code, except returns"
                f" the PythonObjectType docstring instead of raw code.",
                return_direct=True,
            ),
        ]
        return tools
