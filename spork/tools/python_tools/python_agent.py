"""
Python Agent Example

This example demonstrates how to create an autonomous Python agent that can perform Python tasks
using Language Learning Models (LLMs), PythonParser, and PythonWriter.

Example:
    from ...config import *  # noqa F403
    from .python_parser_tool_builder import PythonParserToolBuilder
    from .python_writer_tool_builder import PythonWriterToolBuilder

    python_parser = PythonParser()
    python_writer = PythonWriter(python_parser)

    exec_tools = PythonParserToolBuilder(python_parser).build_tools()
    exec_tools += PythonWriterToolBuilder(python_writer).build_tools()
    python_agent = PythonAgent(exec_tools)

    python_code_overview = python_parser.get_overview()
    instruction_payload = {
        "instruction": "My First Instruction",
        "overview": python_code_overview,
    }

    python_agent.run_agent(instruction_payload)
"""
import os
import time
from typing import Dict, Sequence

from langchain.agents import AgentType, initialize_agent
from langchain.callbacks.base import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import load_prompt
from langchain.tools.base import BaseTool

from ..agents.agent_configs.agent_version import AgentVersion
from ..agents.agent_manager import AgentManager
from .python_parser import PythonParser
from .python_writer import PythonWriter


class PythonAgent:
    """
    The PythonAgent class is responsible for creating an autonomous agent that
    can carry out Python tasks. The agent utilizes a Language Learning Model (LLM),
    a PythonParser, and a PythonWriter to plan and execute Python code.

    Attributes:
        parser (PythonParser): An instance of the PythonParser class.
        writer (PythonWriter): An instance of the PythonWriter class.
        agent_version (AgentVersion): The version of the agent.
        exec_tools (Sequence[BaseTool]): A sequence of execution tools.
        agent (Agent): The initialized agent instance.
    """

    def __init__(
        self,
        exec_tools: Sequence[BaseTool],
        agent_version: AgentVersion = AgentVersion.RETRIEVAL_V1,
        model="gpt-4",
        agent_type=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    ):
        """
        Initializes a PythonAgent instance.

        Args:
            exec_tools (Sequence[BaseTool]): A sequence of execution tools.
            agent_version (AgentVersion, optional): The version of the agent.
                Defaults to AgentVersion.RETRIEVAL_V1.
            model (str, optional): The LLM model to use. Defaults to "gpt-4".
            agent_type (AgentType, optional): The type of agent to create.
                Defaults to AgentType.CONVERSATIONAL_REACT_DESCRIPTION.
        """

        self.parser = PythonParser()
        self.writer = PythonWriter(self.parser)
        self.agent_version = agent_version
        self.exec_tools = exec_tools

        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

        llm = ChatOpenAI(
            temperature=0.7,
            model=model,
            streaming=True,
            verbose=True,
            callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
        )

        self.agent = initialize_agent(
            exec_tools,
            llm,
            agent=agent_type,
            verbose=True,
            memory=memory,
        )

    def build_prompt(self, instruction_payload: Dict[str, str]):
        path = os.getcwd()
        tools = f" {[(tool.name, tool.description) for tool in self.exec_tools]}.\n"

        if self.agent_version == AgentVersion.PYTHON_V1:
            file_tree_exec = os.popen(
                'tree . -I "__pycache__*|*.pyc|__init__.py|local_env|*.egg-info"'
            )
            file_tree = file_tree_exec.read()
            payload = {
                "file_tree": file_tree,
                "path": path,
                "tools": tools,
                "instruction": instruction_payload["instruction"],
            }
        elif self.agent_version == AgentVersion.RETRIEVAL_V1:
            payload = {
                "tools": tools,
                "instruction": instruction_payload["instruction"],
                "overview": instruction_payload["overview"],
            }

        prompt = load_prompt(
            AgentManager.format_config_path("agent_configs", f"{self.agent_version.value}.yaml")
        )
        formatted_prompt = prompt.format(**payload)

        print(f"INFO - PythonAgent is running with initial prompt:\n\n{formatted_prompt}")
        return formatted_prompt

    def run_agent(self, instruction_payload: Dict[str, str]) -> str:
        approved = False
        run_task = self.build_prompt(instruction_payload)
        while not approved:
            try:
                instructions = self.agent.run(run_task)
                run_task = instructions
            except Exception as e:
                print("Exception:", e)
                instructions = (
                    "The previous action created an exception %s. If the exception message contained 'Could not parse LLM output:', the error was likely due to resposne formatting."
                    % e
                )
            time.sleep(1)

        return "Success"


if __name__ == "__main__":
    from ...config import *  # noqa F403
    from .python_parser_tool_builder import PythonParserToolBuilder
    from .python_writer_tool_builder import PythonWriterToolBuilder

    python_parser = PythonParser()
    exec_tools = []
    exec_tools += PythonParserToolBuilder(python_parser).build_tools()
    python_writer = PythonWriter(python_parser)
    exec_tools += PythonWriterToolBuilder(python_writer).build_tools()
    overview = python_parser.get_overview()
    instruction_payload = {
        "instruction": "Write a file called python_agent_tool_builder.py that mimics the workflow of python_parser_tool_builder.py, in the same directory, but which uses the PythonAgent to implement a single function called python-agent-python-task. Be sure to include a sensible description. You should begin this task by inspecting necessary docstrings",
        "overview": overview,
    }
    python_agent = PythonAgent(exec_tools)
    python_agent.run_agent(instruction_payload)
