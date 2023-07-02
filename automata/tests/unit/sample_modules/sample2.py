from typing import List

from tools.python_tools.python_agent import PythonAgent

from automata.core.tools.base import Tool


class PythonAgentToolkit:
    """A class for building tools to interact with PythonAgent."""

    def __init__(self, python_agent: PythonAgent):
        """
        Initializes a PythonAgentToolkit with the given PythonAgent.

        Args:
            python_agent (PythonAgent): A PythonAgent instance representing the agent to work with.
        """
        self.python_agent = python_agent

    def build(self) -> List:
        """
        Builds a list of Tool objects for interacting with PythonAgent.

        Args:
            - None

        Returns:
            - tools (List[Tool]): A list of Tool objects representing PythonAgent commands.
        """

        def python_agent_python_task():
            """A sample task that utilizes PythonAgent."""
            pass

        tools = [
            Tool(
                "automata-task",
                python_agent_python_task,  # type: ignore
                "Execute a Python task using the PythonAgent. Provide the task description in plain English.",
            )
        ]
        return tools
