"""
PythonIndexerToolManager

A class for interacting with the PythonIndexer API, which provides functionality to extract
information about classes, functions, and their docstrings from a given directory of Python files.

The PythonIndexerToolManager class builds a list of Tool objects, each representing a specific
command to interact with the PythonIndexer API.

Attributes:
- python_parser (PythonIndexer): A PythonIndexer object representing the code parser to work with.
- logger (Optional[PassThroughBuffer]): An optional PassThroughBuffer object to log output.

Example usage:
    python_parser = PythonIndexer()
    python_parser_tool_builder = PythonIndexerToolManager(python_parser)
    tools = python_parser_tool_builder.build_tools()

"""

from typing import List, Optional

from langchain.agents import Tool

from ..python_tools.python_indexer import PythonIndexer
from ..utils import PassThroughBuffer
from .base_tool_manager import BaseToolManager


class PythonIndexerToolManager(BaseToolManager):
    """
    PythonIndexerToolManager
    A class for interacting with the PythonIndexer API, which provides functionality to read
    the code state of a of local Python files.
    """

    def __init__(self, python_indexer: PythonIndexer, logger: Optional[PassThroughBuffer] = None):
        """
        Initializes a PythonIndexerToolManager object with the given inputs.

        Args:
        - python_indexer (PythonIndexer): A PythonIndexer object which indexes the code to work with.
        - logger (Optional[PassThroughBuffer]): An optional PassThroughBuffer object to log output.

        Returns:
        - None
        """
        self.python_indexer = python_indexer
        self.logger = logger

    def build_tools(self) -> List[Tool]:
        """
        Builds a list of Tool objects for interacting with PythonIndexer.

        Args:
        - None

        Returns:
        - tools (List[Tool]): A list of Tool objects representing PythonIndexer commands.
        """
        tools = [
            Tool(
                name="python-indexer-get-code",
                func=lambda object_py_path: self.python_indexer.get_raw_code(object_py_path),
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
                name="python-indexer-get-docstring",
                func=lambda object_py_path: self.python_indexer.get_docstring(object_py_path),
                description=f"Identical to python-indexer-get-pyobject-code, except returns"
                f" the docstring instead of raw code.",
                return_direct=True,
                verbose=True,
            ),
        ]
        return tools
