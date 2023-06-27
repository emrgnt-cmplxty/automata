import logging
from typing import List, Optional

from automata.config.base import LLMProvider
from automata.core.agent.tool.registry import AutomataOpenAIAgentToolBuilderRegistry
from automata.core.base.agent import AgentToolBuilder, AgentToolProviders
from automata.core.base.tool import Tool
from automata.core.coding.py.writer import PyWriter
from automata.core.llm.providers.openai import OpenAIAgentToolBuilder, OpenAITool

logger = logging.getLogger(__name__)


class PyWriterToolBuilder(AgentToolBuilder):
    """
    A class for interacting with the PythonWriter API,
    which provides functionality to modify python code.
    """

    def __init__(
        self,
        py_writer: PyWriter,
        do_write: bool = True,
        *args,
        **kwargs,
    ) -> None:
        self.writer = py_writer
        self.do_write = do_write

    def build(self) -> List[Tool]:
        """Builds a suite of tools for writing python code."""
        return [
            Tool(
                name="py-writer-update-module",
                function=self._update_existing_module,
                description=f"Inserts or updates the python code of a function, class, method in an existing module."
                f" If a given object or its child object do not exist, they are created automatically."
                f" If the object already exists, then the existing code is modified. For example,"
                f' to implement a method "my_method" of "MyClass" in the module "my_file.py" which exists in "my_folder",'
                f" the correct tool input follows:\n"
                f'{{"arguments": ["my_folder.my_file", "MyClass", "def my_method():\\n   \\"My Method\\"\\"\\n    print(\\"hello world\\")\\n"]}}'
                f" If new import statements are necessary, then introduce them at the top of the submitted input code."
                f" Provide the full code as input, as this tool has no context outside of passed arguments.\n",
            ),
            Tool(
                name="py-writer-create-new-module",
                function=self._create_new_module,
                description=f"Creates a new module at the given path with the given code. For example,"
                f'{{"arguments": ["my_folder.my_file", "import math\\ndef my_method():\\n   \\"My Method\\"\\"\\n    print(math.sqrt(4))\\n"]}}',
            ),
            Tool(
                name="py-writer-delete-from-existing-module",
                function=self._delete_from_existing_module,
                description=f"Deletes python objects and their code by name from existing module. For example,"
                f'{{"arguments": ["my_folder.my_file", "MyClass.my_method"]}}',
            ),
        ]

    def _update_existing_module(
        self,
        module_dotpath: str,
        disambiguator: Optional[str],
        code: str,
    ) -> str:
        """Updates an existing module with the given code."""
        try:
            self.writer.update_existing_module(module_dotpath, code, disambiguator, self.do_write)
            return "Success"
        except Exception as e:
            return f"Failed to update the module with error - {str(e)}"

    def _delete_from_existing_module(
        self,
        module_dotpath: str,
        object_dotpath: str,
    ) -> str:
        """Deletes an object from an existing module."""
        try:
            self.writer.delete_from_existing__module(module_dotpath, object_dotpath, self.do_write)
            return "Success"
        except Exception as e:
            return f"Failed to reduce the module with error - {str(e)}"

    def _create_new_module(self, module_dotpath: str, code: str) -> str:
        """Creates a new module with the given code."""

        try:
            self.writer.create_new_module(module_dotpath, code, self.do_write)
            return "Success"
        except Exception as e:
            return f"Failed to create the module with error - {str(e)}"


@AutomataOpenAIAgentToolBuilderRegistry.register_tool_manager
class PyWriterOpenAIToolBuilder(PyWriterToolBuilder, OpenAIAgentToolBuilder):
    TOOL_TYPE = AgentToolProviders.PY_WRITER
    PLATFORM = LLMProvider.OPENAI

    def build_for_open_ai(self) -> List[OpenAITool]:
        tools = super().build()

        properties = {
            "module_dotpath": {
                "type": "string",
                "description": "The path to the module to write or modify code.",
            },
            "object_dotpath": {
                "type": "string",
                "description": "The path to the object to write or modify code.",
            },
            "code": {
                "type": "string",
                "description": "The code to write or modify in the object.",
            },
        }

        required = ["module_dotpath", "code"]

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
