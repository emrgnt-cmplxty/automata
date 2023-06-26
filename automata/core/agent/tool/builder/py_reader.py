import logging
from typing import List, Optional

from automata.core.agent.tool.registry import AutomataOpenAIAgentToolBuilderRegistry
from automata.core.base.agent import AgentToolBuilder, AgentToolProviders
from automata.core.base.tool import Tool
from automata.core.coding.py.module_loader import NO_RESULT_FOUND_STR
from automata.core.coding.py.reader import PyReader
from automata.core.llm.providers.available import LLMPlatforms
from automata.core.llm.providers.openai import OpenAIAgentToolBuilder, OpenAITool

logger = logging.getLogger(__name__)


class PyReaderToolBuilder(AgentToolBuilder):
    """
    PyReaderToolBuilder
    A class for interacting with the PythonIndexer API, which provides functionality to read
    the code state of a of local Python files.
    """

    def __init__(self, py_reader: PyReader, **kwargs) -> None:
        """
        Initializes a PyReaderToolBuilder object with the given inputs.

        Args:
        - py_reader (PyReader): A PyReader object which allows inspecting of local code.

        Returns:
        - None
        """
        self.py_reader = py_reader

    def build(self) -> List[Tool]:
        """
        Builds the tools associated with the python code retriever.

        Returns:
            List[Tool]: The list of built tools.
        """
        return [
            Tool(
                name="py-retriever-retrieve-code",
                function=self._run_indexer_retrieve_code,
                description=f"Returns the code of the python package, module, standalone function, class,"
                f" or method at the given python path, without docstrings."
                f' If no match is found, then "{NO_RESULT_FOUND_STR}" is returned.\n\n'
                f'For example - suppose the function "my_function" is defined in the file "my_file.py" located in the main working directory,'
                f"Then the correct tool input for the parser follows:\n"
                f"  - tool_args\n"
                f"    - my_file\n"
                f"    - None\n"
                f"    - my_function\n\n"
                f"Suppose instead the file is located in a subdirectory called my_directory,"
                f" then the correct tool input for the parser is:\n"
                f"  - tool_args\n    - my_directory.my_file\n    - my_function\n\n"
                f"Lastly, if the function is defined in a class, MyClass, then the correct tool input is:\n"
                f"  - tool_args\n    - my_directory.my_file\n    - MyClass.my_function\n\n",
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
        PythonIndexer retrieves the code of the python package,
         module, standalone function, class, or method at the given
         python path, without docstrings.

        Args:
            - module_path (str): The path to the module to retrieve code from.
            - object_path (Optional[str]): The path to the object to retrieve code from.

        Returns:
            - str: The code of the python package, module,
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
        PythonIndexer retrieves the docstring of the python package,
         module, standalone function, class, or method at the given
         python path, without docstrings.

         Args:
            - module_path (str): The path to the module to retrieve code from.
            - object_path (Optional[str]): The path to the object to retrieve code from.

        Returns:
            - str: The docstring of the python package, module,
        """
        try:
            return self.py_reader.get_docstring(module_path, object_path)
        except Exception as e:
            return f"Failed to retrieve docstring with error - {str(e)}"

    def _run_indexer_retrieve_raw_code(
        self, module_path: str, object_path: Optional[str] = None
    ) -> str:
        """
        PythonIndexer retrieves the raw code of the python package,
         module, standalone function, class, or method at the given
         python path, with docstrings.

        Args:
            - module_path (str): The path to the module to retrieve code from.
            - object_path (Optional[str]): The path to the object to retrieve code from.

        Returns:
            - str: The raw code of the python package, module,
        """
        try:
            return self.py_reader.get_source_code(module_path, object_path)
        except Exception as e:
            return f"Failed to retrieve raw code with error - {str(e)}"


@AutomataOpenAIAgentToolBuilderRegistry.register_tool_manager
class PyReaderOpenAIToolBuilder(PyReaderToolBuilder, OpenAIAgentToolBuilder):
    TOOL_TYPE = AgentToolProviders.PY_READER
    PLATFORM = LLMPlatforms.OPENAI

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
