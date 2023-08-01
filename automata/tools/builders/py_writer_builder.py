import ast
import logging
from typing import List

from automata.agent.agent import AgentToolkitBuilder, AgentToolkitNames
from automata.agent.openai_agent import OpenAIAgentToolkitBuilder
from automata.code_writers.py import PyCodeWriter
from automata.config.config_base import LLMProvider
from automata.llm.providers.openai_llm import OpenAITool
from automata.singletons.py_module_loader import py_module_loader
from automata.singletons.toolkit_registry import (
    OpenAIAutomataAgentToolkitRegistry,
)
from automata.tools.tool_base import Tool

logger = logging.getLogger(__name__)


class PyCodeWriterToolkitBuilder(AgentToolkitBuilder):
    """
    A class for interacting with the PythonWriter API,
    which provides functionality to modify python code.
    """

    def __init__(
        self,
        py_writer: PyCodeWriter,
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
                name="update-module",
                function=self._update_existing_module,
                description=f"Inserts or updates the python code of a function, class, method in an existing module."
                f" If a given object or its child object do not exist, they are created automatically."
                f" If the object already exists, then the existing code is modified. For example,"
                f' to implement a method "my_method" of "MyClass" in the module "my_file.py" which exists in "my_folder",'
                f" the correct tool input follows:\n"
                f'{{"arguments": ["my_folder.my_file.MyClass", "def my_method():\\n   \\"My Method\\"\\"\\n    print(\\"hello world\\")\\n"]}}'
                f" If new import statements are necessary, then introduce them at the top of the submitted input code."
                f" Provide the full code as input, as this tool has no context outside of passed arguments.\n",
            ),
            Tool(
                name="create-new-module",
                function=self._create_new_module,
                description=f"Creates a new module at the given path with the given code. For example,"
                f'{{"arguments": ["my_folder.my_file", "import math\\ndef my_method():\\n   \\"My Method\\"\\"\\n    print(math.sqrt(4))\\n"]}}',
            ),
        ]

    # FIXME - Should try / catch be here or upstream in the agent?
    def _update_existing_module(
        self,
        module_dotpath: str,
        code: str,
    ) -> str:
        """Updates an existing module with the given code."""
        try:
            module = py_module_loader.fetch_ast_module(module_dotpath)
            if not module:
                raise KeyError("Module not found in module loader.")
            self.writer.upsert_to_module(module, ast.parse(code))
            self.writer.write_module_to_disk(module_dotpath)

            return "Success"
        except Exception as e:
            return f"Failed to update the module with error - {str(e)}"

    def _create_new_module(self, module_dotpath: str, code: str) -> str:
        """Creates a new module with the given code."""

        try:
            self.writer.create_new_module(
                module_dotpath, ast.parse(code), self.do_write
            )
            return "Success"
        except Exception as e:
            return f"Failed to create the module with error - {str(e)}"


@OpenAIAutomataAgentToolkitRegistry.register_tool_manager
class PyCodeWriterOpenAIToolkitBuilder(
    PyCodeWriterToolkitBuilder, OpenAIAgentToolkitBuilder
):
    TOOL_NAME = AgentToolkitNames.PY_WRITER
    LLM_PROVIDER = LLMProvider.OPENAI

    def build_for_open_ai(self) -> List[OpenAITool]:
        tools = super().build()

        properties = {
            "module_dotpath": {
                "type": "string",
                "description": "The path to the module to write or modify code.",
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
