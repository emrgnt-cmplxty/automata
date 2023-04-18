from typing import List, Optional

from spork.buffer import PassThroughBuffer
from spork.tools.python_tools.python_agent import PythonAgent
from spork.tools.tool import Tool


class PythonAgentToolBuilder:
    def __init__(self, python_agent: PythonAgent, logger: Optional[PassThroughBuffer] = None):
        self.python_agent = python_agent
        self.logger = logger

    def build_tools(self) -> List[Tool]:
        tools = [
            Tool(
                name="python-agent-python-task",
                func=lambda task: self.python_agent.run_agent(task),
                description=f"A single function that uses PythonAgent to perform a given task.",
                return_direct=True,
            )
        ]
        return tools
