"""
CodeParserToolBuilder

A class for interacting with the CodeParser API, which provides functionality to extract
information about classes, functions, and their docstrings from a given directory of Python files.

The CodeParserToolBuilder class builds a list of Tool objects, each representing a specific
command to interact with the CodeParser API.

Attributes:
- code_parser (CodeParser): A CodeParser object representing the code parser to work with.
- logger (Optional[PassThroughBuffer]): An optional PassThroughBuffer object to log output.

Example usage:
    code_parser = CodeParser(os.path.join(home_path(), "your_directory"))
    code_parser_tool_builder = CodeParserToolBuilder(code_parser)
    tools = code_parser_tool_builder.build_tools()

"""

from typing import List, Optional

from langchain.agents import Tool

from ..utils import PassThroughBuffer
from .parser import CodeParser


class CodeParserToolBuilder:
    def __init__(self, code_parser: CodeParser, logger: Optional[PassThroughBuffer] = None):
        """
        Initializes a CodeParserToolBuilder object with the given inputs.

        Args:
        - code_parser (CodeParser): A CodeParser object representing the code parser to work with.
        - logger (Optional[PassThroughBuffer]): An optional PassThroughBuffer object to log output.

        Returns:
        - None
        """
        self.code_parser = code_parser
        self.logger = logger

    def build_tools(self) -> List[Tool]:
        """
        Builds a list of Tool objects for interacting with CodeParser.

        Args:
        - None

        Returns:
        - tools (List[Tool]): A list of Tool objects representing CodeParser commands.
        """
        tools = [
            Tool(
                name="code-parser-lookup-code",
                func=lambda object_name: self.code_parser.lookup_code(object_name),
                description='Returns the raw code of the function or class with the given name, or "No results found" if there is no match found.',
                return_direct=True,
            ),
            Tool(
                name="code-parser-lookup-docstring",
                func=lambda object_name: self.code_parser.lookup_docstring(object_name),
                description='Returns the docstring of the function or class with the given name, or  "No results found" if there is no match found.',
                return_direct=True,
            ),
            Tool(
                name="code-parser-get-standalone-functions",
                func=lambda file_name: ", ".join(
                    self.code_parser.get_standalone_functions(file_name)
                ),
                description='Returns the list of standalone function names for the given file, or a list with the single entry "No results found" if the file is not found or if it contains no standalone functions.',
                return_direct=True,
            ),
            Tool(
                name="code-parser-get-classes",
                func=lambda file_name: ", ".join(self.code_parser.get_classes(file_name)),
                description='Returns the list of class names in a file, or a list with the single entry "No results found" if the file is not found or if it contains no classes.',
                return_direct=True,
            ),
            Tool(
                name="code-parser-lookup-file-docstring",
                func=lambda file_name: self.code_parser.lookup_file_docstring(file_name),
                description='Returns the docstring of a file, or "No results found" if the file is not found or if it contains no docstring.',
                return_direct=True,
            ),
            Tool(
                name="code-parser-build-file-summary",
                func=lambda file_name: self.code_parser.build_file_summary(file_name),
                description='Returns a formatted summary of the specified file, or "No results found" if the file is not found or if there is nothing to summarize. A valid summary returns the concatenated docstrings of standalone functions, classes and their respective functions, and any nested classes.',
                return_direct=True,
            ),
        ]
        return tools
