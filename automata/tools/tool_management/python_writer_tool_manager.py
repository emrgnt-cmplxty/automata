"""
PythonWriterToolManager

A class for interacting with the PythonWriter API, which provides functionality to modify
the code state of a given directory of Python files.

Attributes:
- writer (PythonWriter): A PythonWriter object for manipulating local pythonf iles.

Example - 
    Build a list of Tool objects for interacting with PythonWriter:
    python_indexer = PythonIndexer(root_py_path())
    python_writer = PythonWriter(python_indexer)
    python_writer_tool_manager = PythonWriterToolManager(python_writer)
    tools = build_tools(tool_manager)
"""
import logging
from typing import List

from automata.configs.agent_configs import AgentConfig
from automata.core.base.tool import Tool

from ..python_tools.python_writer import PythonWriter
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
        self.automata_version = kwargs.get("automata_version") or AgentConfig.AUTOMATA_WRITER_V2
        self.model = kwargs.get("model") or "gpt-4"
        self.verbose = kwargs.get("verbose") or False
        self.stream = kwargs.get("stream") or True
        self.temperature = kwargs.get("temperature") or 0.7

    def writer_update_module(self, input_str: str) -> str:
        module_path = input_str.split(",")[0]
        class_name = input_str.split(",")[1]
        code = ",".join(input_str.split(",")[2:]).strip()
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

    def automata_update_module(self, input_str: str) -> str:
        from automata.core import load_llm_toolkits
        from automata.core.agents.automata_agent import AutomataAgent

        try:
            initial_payload = {
                "overview": self.writer.indexer.get_overview(),
            }
            agent = AutomataAgent(
                initial_payload=initial_payload,
                instructions=input_str,
                llm_toolkits=load_llm_toolkits(["python_writer"]),
                version=self.automata_version,
                model=self.model,
                stream=self.stream,
                verbose=self.verbose,
                temperature=self.temperature,
            )
            agent.run()

            return "Success"
        except Exception as e:
            return "Failed to update the module with error - " + str(e)

    def build_tools(self) -> List[Tool]:
        """
        Builds a list of Tool object for interacting with PythonWriter.

        Args:
        - None

        Returns:
        - tools (List[Tool]): A list of Tool objects representing PythonWriter commands.
        """
        tools = [
            Tool(
                name="python-writer-update-module",
                func=lambda path_comma_code_str: self.writer_update_module(path_comma_code_str),
                description=f"Modifies the python code of a function, class, method, or module after receiving"
                f" an input module path, source code, and optional class name. If the specified object or dependencies do not exist,"
                f" then they are created automatically. If the object already exists,"
                f" then the existing code is modified."
                f" For example -"
                f' to implement a method "my_method" of "MyClass" in the module "my_file.py" which exists in "my_folder",'
                f" the correct function call is"
                f' {{"tool": "python-writer-update-module",'
                f' "input": "my_folder.my_file,MyClass,def my_function() -> None:\n   """My Function"""\n    print("hello world")"}}.'
                f" If new import statements are necessary, then introduce them to the module separately. Do not forget to wrap your input in double quotes.",
                return_direct=True,
            ),
        ]
        return tools

    def build_tools_with_automata(self) -> List[Tool]:
        """
        Builds a list of Tool object for interacting with PythonWriter.

        Args:
        - None

        Returns:
        - tools (List[Tool]): A list of Tool objects representing PythonWriter commands.
        """
        tools = [
            Tool(
                name="automata-writer-modify-module",
                func=lambda path_comma_code_str: self.automata_update_module(path_comma_code_str),
                description=f"Modifies the python code of a function, class, method, or module after receiving"
                f" an input module path, source code, and optional class name. The actual work is carried out by an autonomous agent called Automata.",
            ),
        ]
        return tools
