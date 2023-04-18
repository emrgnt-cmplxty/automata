from typing import List

from langchain.agents import Tool

from spork.tools.python_tools.python_agent import PythonAgent


class PythonAgentToolBuilder:
    """A class for building tools to interact with PythonAgent."""

    def __init__(self, python_agent: PythonAgent):
        """
        Initializes a PythonAgentToolBuilder with the given PythonAgent.

        Args:
            python_agent (PythonAgent): A PythonAgent instance representing the agent to work with.
            logger (logging.Logger): An optional logger to log output.
        """
        self.python_agent = python_agent

    def build_tools(self) -> List:
        """
        Builds a list of Tool PythonObjects for interacting with PythonAgent.

        Args:
            - None

        Returns:
            - tools (List[Tool]): A list of Tool PythonObjects representing PythonAgent commands.
        """

        def python_agent_python_task():
            """A sample task that utilizes PythonAgent."""
            pass

        tools = [
            Tool(
                "mr-meeseeks-task",
                python_agent_python_task,
                "Execute a Python task using the PythonAgent. Provide the task description in plain English.",
            )
        ]
        return tools
