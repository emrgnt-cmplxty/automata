"""
PythonParserToolManager

A class for interacting with the PythonParser API, which provides functionality to extract
information about classes, functions, and their docstrings from a given directory of Python files.

The PythonParserToolManager class builds a list of Tool objects, each representing a specific
command to interact with the PythonParser API.

Attributes:
- python_parser (PythonParser): A PythonParser object representing the code parser to work with.
- logger (Optional[PassThroughBuffer]): An optional PassThroughBuffer object to log output.

Example usage:
    python_parser = PythonParser()
    python_parser_tool_builder = PythonParserToolManager(python_parser)
    tools = python_parser_tool_builder.build_tools()

"""

from typing import List, Optional

from langchain.agents import Tool

from ..python_tools.python_parser import PythonParser
from ..utils import PassThroughBuffer
from .base_tool_manager import BaseToolManager


class PythonParserToolManager(BaseToolManager):
    """
    PythonParserToolManager
    A class for interacting with the PythonParser API, which provides functionality to read
    the code state of a of local Python files.
    """

    def __init__(self, python_parser: PythonParser, logger: Optional[PassThroughBuffer] = None):
        """
        Initializes a PythonParserToolManager object with the given inputs.

        Args:
        - python_parser (PythonParser): A PythonParser object representing the code parser to work with.
        - logger (Optional[PassThroughBuffer]): An optional PassThroughBuffer object to log output.

        Returns:
        - None
        """
        self.python_parser = python_parser
        self.logger = logger

    def build_tools(self) -> List[Tool]:
        """
        Builds a list of Tool objects for interacting with PythonParser.

        Args:
        - None

        Returns:
        - tools (List[Tool]): A list of Tool objects representing PythonParser commands.
        """
        tools = [
            Tool(
                name="python-parser-get-raw-code",
                func=lambda object_py_path: self.python_parser.get_raw_code(object_py_path),
                description=f"Returns the code of the python package, module,"
                f" standalone function, class, or method at the given python path, without docstrings."
                f' "No results found" is returned if no match is found.\n'
                f' For example - suppose the function "my_function" is defined in the file "my_file.py"'
                f" located in the main working directory, then the correct tool input is my_file.my_function"
                f" Suppose instead the file is located in a subdirectory called my_directory,"
                f' then the correct tool input for the parser is "my_directory.my_file.my_function".',
                return_direct=True,
                verbose=True,
            ),
            Tool(
                name="python-parser-get-docstring",
                func=lambda object_py_path: self.python_parser.get_docstring(object_py_path),
                description=f"Identical to python-parser-get-pyobject-code, except returns"
                f" the docstring instead of raw code.",
                return_direct=True,
                verbose=True,
            ),
        ]
        return tools
