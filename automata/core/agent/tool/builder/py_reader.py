import logging
from typing import List, Optional

from automata.config.base import LLMProvider
from automata.core.agent.tool.registry import AutomataOpenAIAgentToolBuilderRegistry
from automata.core.base.agent import AgentToolBuilder, AgentToolProviders
from automata.core.base.tool import Tool
from automata.core.coding.py.module_loader import NO_RESULT_FOUND_STR
from automata.core.coding.py.reader import PyReader
from automata.core.llm.providers.openai import OpenAIAgentToolBuilder, OpenAITool

logger = logging.getLogger(__name__)


class PyReaderToolBuilder(AgentToolBuilder):
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
                name="py-retriever-retrieve-code",
                function=self._run_indexer_retrieve_code,
                description=f"Returns the code of the python package, module, standalone function, class,"
                f" or method at the given python path, without docstrings."
                f' If no match is found, then "{NO_RESULT_FOUND_STR}" is returned.\n\n'
                f'For example - suppose the function "my_function" is defined in the file "my_file.py" located in the main working directory,'
                f"then the correct tool input is:\n"
                f'arguments: {{"module_path": "my_file", "object_path": "my_file"}}'
                f"Suppose instead the file is located in a subdirectory called my_directory:\n"
                f'arguments: {{"module_path": "my_directory.my_file", "object_path": "my_function"}}'
                f"Lastly, if the function is defined in a class, MyClass, then the correct tool input is:\n"
                f'arguments: {{"module_path": "my_file", "object_path": "MyClass.my_function"}}',
            ),
            Tool(
                name="py-retriever-retrieve-docstring",
                function=self._run_indexer_retrieve_docstring,
                description="Identical to py-retriever-retrieve-code, except returns the docstring instead of raw code.",
            ),
            Tool(
                name="py-retriever-retrieve-raw-code",
                function=self._run_indexer_retrieve_raw_code,
                description="Identical to py-retriever-retrieve-code, except returns the raw text (e.g. code + docstrings) of the module.",
            ),
        ]

    def _run_indexer_retrieve_code(
        self, module_path: str, object_path: Optional[str] = None
    ) -> str:
        """
        Retrieves the code of the python package, module,
        standalone function, class, or method at the given
        python path, without docstrings.
        """
        try:
            return self.py_reader.get_source_code_without_docstrings(module_path, object_path)
        except Exception as e:
            return f"Failed to retrieve code with error - {str(e)}"

    def _run_indexer_retrieve_docstring(
        self, module_path: str, object_path: Optional[str] = None
    ) -> str:
        """
        Retrieves the docstrings python package, module,
        standalone function, class, or method at the given
        python path, without docstrings.
        """
        try:
            return self.py_reader.get_docstring(module_path, object_path)
        except Exception as e:
            return f"Failed to retrieve docstring with error - {str(e)}"

    def _run_indexer_retrieve_raw_code(
        self, module_path: str, object_path: Optional[str] = None
    ) -> str:
        """
        Retrieves the raw code of the python package,
        module, standalone function, class, or method at the given
        python path, with docstrings.
        """
        try:
            return self.py_reader.get_source_code(module_path, object_path)
        except Exception as e:
            return f"Failed to retrieve raw code with error - {str(e)}"


@AutomataOpenAIAgentToolBuilderRegistry.register_tool_manager
class PyReaderOpenAIToolBuilder(PyReaderToolBuilder, OpenAIAgentToolBuilder):
    TOOL_TYPE = AgentToolProviders.PY_READER
    PLATFORM = LLMProvider.OPENAI

    def build_for_open_ai(self) -> List[OpenAITool]:
        tools = super().build()

        properties = {
            "module_path": {
                "type": "string",
                "description": "The path to the module to retrieve code from.",
            },
            "object_path": {
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
