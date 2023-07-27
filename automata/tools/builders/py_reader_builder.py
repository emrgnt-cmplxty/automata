import logging
from typing import List, Optional

from automata.agent.agent import AgentToolkitBuilder, AgentToolkitNames
from automata.agent.openai_agent import OpenAIAgentToolkitBuilder
from automata.code_parsers.py import PyReader
from automata.config.config_base import LLMProvider
from automata.llm.providers.openai_llm import OpenAITool
from automata.singletons.toolkit_registry import (
    OpenAIAutomataAgentToolkitRegistry,
)
from automata.tools.tool_base import Tool

logger = logging.getLogger(__name__)


class PyReaderToolkitBuilder(AgentToolkitBuilder):
    """
    A class for interacting with the PythonIndexer API,
    which provides functionality to retrieve python code.
    """

    def __init__(self, py_reader: PyReader, **kwargs) -> None:
        self.py_reader = py_reader

    def build(self) -> List[Tool]:
        """Builds tools associated with directly retrieving python code."""

        return [
            Tool(
                name="py-retriever-code",
                function=self._run_indexer_retrieve_code,
                description=f"Returns the code of the python package, module, standalone function, class,"
                f" or method at the given module path and sub-module (e.g. node) path."
                f' If no match is found, then "{PyReader.NO_RESULT_FOUND_STR}" is returned.\n\n'
                f'For example - suppose we want the entire source code of a module located in "target_module.py" of the root directory,'
                f"then the correct tool input is:\n"
                f'arguments: {{"module_path": "target_module"}}'
                f"Suppose instead the file is located in a subdirectory called module_directory:\n"
                f'arguments: {{"module_path": "module_directory.target_module"}}'
                f"Next, suppose that we just want to retrieve 'target_function' in target_module:"
                f'arguments: {{"module_path": "module_directory.target_module", "node_path": "target_function"}}'
                f"Lastly, if the function is defined in a class, TargetClass, then the correct tool input is:\n"
                f'arguments: {{"module_path": "module_directory.target_module", "node_path": "TargetClass.target_function"}}',
            ),
            Tool(
                name="py-retriever-retrieve-docstring",
                function=self._run_indexer_retrieve_docstring,
                description="Identical to py-retriever-retrieve-code, except returns the docstring instead of raw code.",
            ),
        ]

    def _run_indexer_retrieve_code(
        self, module_path: str, node_path: Optional[str] = None
    ) -> str:
        """
        Retrieves the code of the python package, module,
        standalone function, class, or method at the given
        python path, without docstrings.
        """
        try:
            return self.py_reader.get_source_code(module_path, node_path)
        except Exception as e:
            return f"Failed to retrieve code with error - {str(e)}"

    def _run_indexer_retrieve_docstring(
        self, module_path: str, node_path: Optional[str] = None
    ) -> str:
        """
        Retrieves the docstrings python package, module,
        standalone function, class, or method at the given
        python path, without docstrings.
        """
        try:
            return self.py_reader.get_docstring(module_path, node_path)
        except Exception as e:
            return f"Failed to retrieve docstring with error - {str(e)}"


@OpenAIAutomataAgentToolkitRegistry.register_tool_manager
class PyReaderOpenAIToolkit(PyReaderToolkitBuilder, OpenAIAgentToolkitBuilder):
    TOOL_NAME = AgentToolkitNames.PY_READER
    LLM_PROVIDER = LLMProvider.OPENAI

    def build_for_open_ai(self) -> List[OpenAITool]:
        tools = super().build()

        properties = {
            "module_path": {
                "type": "string",
                "description": "The path to the module to retrieve code from.",
            },
            "node_path": {
                "type": "string",
                "description": "The path to the object to retrieve code from.",
            },
        }

        required = ["module_path"]

        openai_tools = []
        for tool in tools:
            openai_tool = OpenAITool(
                function=tool.function,
                name=tool.name,
                description=tool.description,
                properties=properties,
                required=required,
            )
            openai_tools.append(openai_tool)

        return openai_tools
