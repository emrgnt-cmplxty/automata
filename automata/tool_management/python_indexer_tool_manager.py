"""
PythonIndexerToolManager

A class for interacting with the PythonIndexer API, which provides functionality to extract
information about classes, functions, and their docstrings from a given directory of Python files.

The PythonIndexerToolManager class builds a list of Tool objects, each representing a specific
command to interact with the PythonIndexer API.

Attributes:
- indexer (PythonIndexer): A PythonIndexer object representing the code parser to work with.

Example usage:
    python_indexer = PythonIndexer()
    python_parser_tool_builder = PythonIndexerToolManager(python_parser)
    tools = python_parser_tool_builder.build_tools()

TODO - Do not put codebase-oracle in this workflow, that is a bad hack.
"""
import logging
from typing import Any, List, Optional, Tuple

from automata.configs.agent_configs.config_type import AutomataAgentConfig, AutomataConfigVersion
from automata.core.agents.automata_agent import AutomataAgentBuilder
from automata.core.base.tool import Tool
from automata.tool_management.base_tool_manager import BaseToolManager
from automata.tools.python_tools.python_indexer import PythonIndexer

logger = logging.getLogger(__name__)


class PythonIndexerToolManager(BaseToolManager):
    """
    PythonIndexerToolManager
    A class for interacting with the PythonIndexer API, which provides functionality to read
    the code state of a of local Python files.
    """

    def __init__(self, **kwargs):
        """
        Initializes a PythonIndexerToolManager object with the given inputs.

        Args:
        - python_indexer (PythonIndexer): A PythonIndexer object which indexes the code to work with.

        Returns:
        - None
        """
        self.indexer: PythonIndexer = kwargs.get("python_indexer")
        self.automata_version = (
            kwargs.get("automata_version") or AutomataConfigVersion.AUTOMATA_INDEXER_PROD
        )
        self.model = kwargs.get("model") or "gpt-4"
        self.temperature = kwargs.get("temperature") or 0.7
        self.verbose = kwargs.get("verbose") or False
        self.stream = kwargs.get("stream") or True

    def build_tools(self) -> List[Tool]:
        """Builds a list of Tool objects for interacting with PythonIndexer."""
        tools = [
            Tool(
                name="python-indexer-retrieve-code",
                func=lambda module_object_tuple: self._run_indexer_retrieve_code(
                    *module_object_tuple
                ),
                description=f'Returns the code of the python package, module, standalone function, class, or method at the given python path, without docstrings. "No results found" is returned if no match is found.\n For example - suppose the function "my_function" is defined in the file "my_file.py" located in the main working directory, then the correct tool input is my_file,my_function Suppose instead the file is located in a subdirectory called my_directory, then the correct tool input for the parser is - inputs\n  - my_directory.my_file\n  - my_function. If the function is defined in a class, MyClass, then the correct tool input is - inputs\n  - my_directory.my_file\n  - MyClass.my_function',
                return_direct=True,
                verbose=True,
            ),
            Tool(
                name="python-indexer-retrieve-docstring",
                func=lambda module_object_tuple: self._run_indexer_retrieve_docstring(
                    *module_object_tuple
                ),
                description=f"Identical to python-indexer-retrieve-code, except returns the docstring instead of raw code.",
                return_direct=True,
                verbose=True,
            ),
            Tool(
                name="python-indexer-retrieve-raw-code",
                func=lambda module_object_tuple: self._run_indexer_retrieve_raw_code(
                    *module_object_tuple
                ),
                description=f"Identical to python-indexer-retrieve-code, except returns the raw text (e.g. code + docstrings) of the module.",
                return_direct=True,
                verbose=True,
            ),
        ]
        return tools

    def build_tools_with_automata(self, config: Any) -> List[Tool]:
        """Builds a list of Automata powered Tool objects for interacting with PythonWriter."""
        tools = [
            Tool(
                name="automata-indexer-retrieve-code",
                func=lambda path_str: self._run_automata_indexer_retrieve_code(path_str, config),
                description="Automata parses a natural language query to retrieve the correct code, docstrings, and import statements necessary to solve an abstract task",
            ),
        ]
        return tools

    def _run_indexer_retrieve_code(self, module_path: str, object_path: str) -> str:
        """PythonIndexer retrieves the code of the python package, module, standalone function, class, or method at the given python path, without docstrings."""
        try:
            result = self.indexer.retrieve_code(module_path, object_path)
            return result
        except Exception as e:
            return "Failed to retrieve code with error - " + str(e)

    def _run_indexer_retrieve_docstring(self, module_path: str, object_path: str) -> str:
        """PythonIndexer retrieves the docstring of the python package, module, standalone function, class, or method at the given python path, without docstrings."""
        try:
            result = self.indexer.retrieve_docstring(module_path, object_path)
            return result
        except Exception as e:
            return "Failed to retrieve docstring with error - " + str(e)

    def _run_indexer_retrieve_raw_code(self, module_path: str, object_path: str) -> str:
        """PythonIndexer retrieves the raw code of the python package, module, standalone function, class, or method at the given python path, with docstrings."""
        try:
            result = self.indexer.retrieve_raw_code(module_path, object_path)
            return result
        except Exception as e:
            return "Failed to retrieve raw code with error - " + str(e)

    def _run_automata_indexer_retrieve_code(
        self, input_str: str, automata_config: AutomataAgentConfig
    ) -> str:
        """Automata retrieves the code of the python package, module, standalone function, class, or method at the given python path, without docstrings."""
        from automata.tool_management.tool_management_utils import build_llm_toolkits

        try:
            initial_payload = {"overview": self.indexer.get_overview()}
            agent = (
                AutomataAgentBuilder(automata_config)
                .with_initial_payload(initial_payload)
                .with_instructions(input_str)
                .with_llm_toolkits(build_llm_toolkits(["python_indexer"]))
                .with_model(self.model)
                .with_stream(self.stream)
                .with_verbose(self.verbose)
                .with_temperature(self.temperature)
                .build()
            )
            result = agent.run()
            return result
        except Exception as e:
            return "Failed to retrieve the code with error - " + str(e)

    @staticmethod
    def parse_input_str(input_str: str) -> Tuple[str, Optional[str]]:
        """Parses the input string into a module path and an optional object path."""
        split_input = input_str.split(",")
        module_path = split_input[0].strip()
        if len(split_input) == 1:
            object_path = None
        else:
            object_path = input_str.split(",")[1].strip()
        return (module_path, object_path)
