from typing import List, Optional

from langchain.agents import Tool

from spork.agents.mr_meeseeks_agent import MrMeeseeksAgent
from spork.tools.tool_managers.base_tool_manager import BaseToolManager
from spork.tools.utils import PassThroughBuffer


class MrMeeseeksAgentToolManager(BaseToolManager):
    def __init__(
        self, mr_meeseeks_agent: MrMeeseeksAgent, logger: Optional[PassThroughBuffer] = None
    ):
        self.mr_meeseeks_agent = mr_meeseeks_agent
        self.logger = logger

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
