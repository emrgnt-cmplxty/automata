import os
from typing import Sequence

from langchain.agents import AgentType, initialize_agent
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
    This class consumes an LLM and PythonParser+PythonWriter to create a Python agent.
    The agent can be used to plan and execute Python code.
    """

    def __init__(
        self,
        exec_tools: Sequence[BaseTool],
        agent_version: AgentVersion = AgentVersion.PYTHON_V1,
        model="gpt-3.5-turbo",
        agent_type=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
    ):
        self.parser = PythonParser()
        self.writer = PythonWriter(self.parser)
        self.agent_version = agent_version
        self.exec_tools = exec_tools

        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        llm = ChatOpenAI(temperature=0, model=model)

        self.agent = initialize_agent(
            exec_tools,
            llm,
            agent=agent_type,
            verbose=True,
            memory=memory,
        )

    def build_prompt(self, task):
        if self.agent_version == AgentVersion.PYTHON_V1:
            file_tree_exec = os.popen(
                'tree . -I "__pycache__*|*.pyc|__init__.py|local_env|*.egg-info"'
            )
            file_tree = file_tree_exec.read()
            path = os.getcwd()
            tools = f" {[(tool.name, tool.description) for tool in self.exec_tools]}.\n"
            payload = {
                "file_tree": file_tree,
                "path": path,
                "tools": tools,
                "task": task,
            }
        prompt = load_prompt(
            AgentManager.format_config_path("agent_configs", f"{self.agent_version.value}.yaml")
        )
        formatted_prompt = prompt.format(**payload).replace("\\n", "\n")

        print(f"The PythonAgent is creating the prompt {formatted_prompt} for task {task}")
        return formatted_prompt

    def run_agent(self, task) -> str:
        approved = False
        run_task = self.build_prompt(task)
        while not approved:
            instructions = self.agent.run(run_task)
            print("Created new Instructions:", instructions)
            feedback = input(
                "Do you approve? If approved, type 'y'. If not approved, type why so the agent can try again: "
            )
            approved = feedback == "y"
            run_task = feedback
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

    test_task = "Write a file called python_agent_tool_builder.py that mimics the workflow of prompt_tool_builder.py, in the same directory, but which uses the PythonAgent to implement a single function called python-agent-python-task. Write a reasonable description for this task"
    python_agent = PythonAgent(exec_tools)
    python_agent.run_agent(test_task)
