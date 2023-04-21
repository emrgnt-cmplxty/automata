from typing import List

from langchain.agents import Tool

from spork.agents.mr_meeseeks_agent import MrMeeseeksAgent
from spork.tools.tool_managers.base_tool_manager import BaseToolManager


class MrMeeseeksAgentToolManager(BaseToolManager):
    def __init__(self, mr_meeseeks_agent: MrMeeseeksAgent):
        self.mr_meeseeks_agent = mr_meeseeks_agent

    def build_tools(self) -> List[Tool]:
        tools = [
            Tool(
                name="mr-meeseeks-agent",
                func=lambda: self.mr_meeseeks_agent.run(),
                description="Exposes the run command of the MrMeeseeksAgent class, which runs the task and reports the tool outputs back to the master.",
                example="mr-meeseeks-task",
                return_direct=True,
                verbose=True,
            )
        ]
        return tools

    def build_tools_with_meeseeks(self) -> List[Tool]:
        return []
