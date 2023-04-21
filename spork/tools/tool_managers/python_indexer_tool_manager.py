"""
PythonIndexerToolManager

A class for interacting with the PythonIndexer API, which provides functionality to extract
information about classes, functions, and their docstrings from a given directory of Python files.

The PythonIndexerToolManager class builds a list of Tool objects, each representing a specific
command to interact with the PythonIndexer API.

Attributes:
- python_parser (PythonIndexer): A PythonIndexer object representing the code parser to work with.

Example usage:
    python_parser = PythonIndexer()
    python_parser_tool_builder = PythonIndexerToolManager(python_parser)
    tools = python_parser_tool_builder.build_tools()

TODO - Do not put codebase-oracle in this workflow, that is a bad hack.
"""
from typing import List, Optional, Tuple

from langchain.agents import Tool

from spork.agents.agent_configs.agent_version import AgentVersion
from spork.agents.mr_meeseeks_agent import MrMeeseeksAgent
from spork.tools.oracle.codebase_oracle import CodebaseOracle
from spork.tools.tool_managers.codebase_oracle_tool_manager import CodebaseOracleToolManager

from ..python_tools.python_indexer import PythonIndexer
from .base_tool_manager import BaseToolManager


class PythonIndexerToolManager(BaseToolManager):
    """
    PythonIndexerToolManager
    A class for interacting with the PythonIndexer API, which provides functionality to read
    the code state of a of local Python files.
    """

    def __init__(self, python_indexer: PythonIndexer):
        """
        Initializes a PythonIndexerToolManager object with the given inputs.

        Args:
        - python_indexer (PythonIndexer): A PythonIndexer object which indexes the code to work with.
        - logger (Optional[PassThroughBuffer]): An optional PassThroughBuffer object to log output.

        Returns:
        - None
        """
        self.indexer = python_indexer

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
                name="python-indexer-retrieve-code",
                func=lambda module_comma_object_path: self._indexer_retrieve_code(
                    module_comma_object_path
                ),
                description=f'Returns the code of the python package, module, standalone function, class, or method at the given python path, without docstrings. "No results found" is returned if no match is found.\n For example - suppose the function "my_function" is defined in the file "my_file.py" located in the main working directory, then the correct tool input is my_file,my_function Suppose instead the file is located in a subdirectory called my_directory, then the correct tool input for the parser is "my_directory.my_file,my_function". If the function is defined in a class, MyClass, then the correct tool input is "my_directory.my_file,MyClass.my_function".',
                return_direct=True,
                verbose=True,
            ),
            Tool(
                name="python-indexer-retrieve-docstring",
                func=lambda module_comma_object_path: self._indexer_retrieve_docstring(
                    module_comma_object_path
                ),
                description=f"Identical to python-indexer-retrieve-code, except returns the docstring instead of raw code.",
                return_direct=True,
                verbose=True,
            ),
        ]
        return tools

    def build_tools_with_meeseeks(self) -> List[Tool]:
        tools = [
            Tool(
                name="meeseeks-indexer-retrieve-code",
                func=lambda path_str: self._meeseeks_indexer_retrieve_code(path_str),
                description="Mr. Meeseeks parses a natural language query to retrieve the correct code, docstrings, and import statements necessary to solve an abstract task",
            ),
        ]
        return tools

    def _indexer_retrieve_code(self, input_str: str) -> str:
        try:
            module_path, object_path = self.parse_input_str(input_str)
            result = self.indexer.retrieve_code(module_path, object_path)
            return result
        except Exception as e:
            return "Failed to retrieve code with error - " + str(e)

    def _indexer_retrieve_docstring(self, input_str: str) -> str:
        try:
            module_path, object_path = self.parse_input_str(input_str)
            result = self.indexer.retrieve_docstring(module_path, object_path)
            return result
        except Exception as e:
            return "Failed to retrieve docstring with error - " + str(e)

    def _meeseeks_indexer_retrieve_code(self, path_str: str) -> str:
        """Mr. Meeseeks retrieves the code of the python package, module, standalone function, class, or method at the given python path, without docstrings."""
        try:
            initial_payload = {"overview": self.indexer.get_overview()}
            instructions = f"Retrieve the code for {path_str}"
            agent = MrMeeseeksAgent(
                initial_payload=initial_payload,
                instructions=instructions,
                tools=self.build_tools(),
                version=AgentVersion.MEESEEKS_RETRIEVER_V2,
                model="gpt-4",
                stream=True,
                verbose=False,
            )
            result = agent.run()
            return result
        except Exception as e:
            return "Failed to retrieve the code with error - " + str(e)

    @staticmethod
    def parse_input_str(input_str: str) -> Tuple[str, Optional[str]]:
        split_input = input_str.split(",")
        module_path = split_input[0].strip()
        if len(split_input) == 1:
            object_path = None
        else:
            object_path = input_str.split(",")[1].strip()
        return (module_path, object_path)
