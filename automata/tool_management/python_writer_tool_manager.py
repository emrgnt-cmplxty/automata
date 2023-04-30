"""
PythonWriterToolManager

A class for interacting with the PythonWriter API, which provides functionality to modify
the code state of a given directory of Python files.

Attributes:
- writer (PythonWriter): A PythonWriter object for manipulating local pythonf iles.

Example -
    python_indexer = PythonIndexer(root_py_path())
    python_writer = PythonWriter(python_indexer)
    python_writer_tool_manager = PythonWriterToolManager(python_writer)
    tools = build_tools(tool_manager)
"""
import logging
from typing import Any, List, Optional

from automata.configs.automata_agent_configs import AutomataAgentConfig
from automata.configs.config_enums import AgentConfigVersion
from automata.core.agents.automata_agent_builder import AutomataAgentBuilder
from automata.core.base.tool import Tool
from automata.tools.python_tools.python_writer import PythonWriter

from .base_tool_manager import BaseToolManager

logger = logging.getLogger(__name__)


class PythonWriterToolManager(BaseToolManager):
    """
    PythonWriterToolManager
    A class for interacting with the PythonWriter API, which provides functionality to modify
    the code state of a given directory of Python files.
    """

    def __init__(
        self,
        **kwargs,
    ):
        """
        Initializes a PythonWriterToolManager object with the given inputs.

        Args:
        - writer (PythonWriter): A PythonWriter object representing the code writer to work with.

        Returns:
        - None
        """
        self.writer: PythonWriter = kwargs.get("python_writer")
        self.automata_version = (
            kwargs.get("automata_version") or AgentConfigVersion.AUTOMATA_WRITER_PROD
        )
        self.model = kwargs.get("model") or "gpt-4"
        self.verbose = kwargs.get("verbose") or False
        self.stream = kwargs.get("stream") or True
        self.temperature = kwargs.get("temperature") or 0.7

    def build_tools(self) -> List[Tool]:
        """Builds a list of Tool object for interacting with PythonWriter."""
        tools = [
            Tool(
                name="python-writer-update-module",
                func=lambda module_object_code_tuple: self._writer_update_module(
                    *module_object_code_tuple
                ),
                description=f"Modifies the python code of a function, class, method, or module after receiving"
                f" an input module path, source code, and optional class name. If the specified object or dependencies do not exist,"
                f" then they are created automatically. If the object already exists,"
                f" then the existing code is modified."
                f" For example -"
                f' to implement a method "my_method" of "MyClass" in the module "my_file.py" which exists in "my_folder",'
                f" the correct function call follows:\n"
                f" - tool_query_1\n"
                f"   - tool_name\n"
                f"     - python-writer-update-module\n"
                f"   - tool_args\n"
                f"     - my_folder.my_file\n"
                f"     - MyClass\n"
                f'     - def my_method() -> None:\n   """My Method"""\n    print("hello world")\n'
                f"If new import statements are necessary, then introduce them at the top of the submitted input code.\n"
                f"Provide the full code as input, as this tool has no context outside of passed arguments.\n",
                return_direct=True,
            ),
        ]
        return tools

    def build_tools_with_automata(self, config: Any) -> List[Tool]:
        """Builds a list of Automata powered tool objects for interacting with PythonWriter."""
        tools = [
            Tool(
                name="automata-writer-modify-module",
                func=lambda input_str: self._automata_update_module(input_str, config),
                description=f"Modifies the python code of a function, class, method, or module after receiving"
                f" an input module path, source code, and optional class name. The actual work is carried out by an autonomous agent called Automata.",
            ),
        ]
        return tools

    def _writer_update_module(self, module_path: str, class_name: Optional[str], code: str) -> str:
        """Writes the given code to the given module path and class name."""
        try:
            self.writer.update_module(
                source_code=code,
                extending_module=True,
                module_path=module_path,
                write_to_disk=True,
                class_name=class_name,
            )
            return "Success"
        except Exception as e:
            return "Failed to update the module with error - " + str(e)

    def _automata_update_module(self, input_str: str, automata_config: AutomataAgentConfig) -> str:
        """Creates an AutomataAgent to write the given task."""
        from automata.tool_management.tool_management_utils import build_llm_toolkits

        try:
            initial_payload = {
                "overview": self.writer.indexer.get_overview(),
            }
            agent = (
                AutomataAgentBuilder(automata_config)
                .with_initial_payload(initial_payload)
                .with_instructions(input_str)
                .with_llm_toolkits(build_llm_toolkits(["python_writer"]))
                .with_model(self.model)
                .with_stream(self.stream)
                .with_verbose(self.verbose)
                .with_temperature(self.temperature)
                .build()
            )

            agent.run()

            return "Success"
        except Exception as e:
            return "Failed to update the module with error - " + str(e)
