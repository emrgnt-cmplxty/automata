from typing import List, Optional

from langchain.agents import Tool

from spork.tools.agents.agent_mr_meeseeks import AgentMrMeeseeks
from spork.tools.tool_managers.base_tool_manager import BaseToolManager
from spork.tools.utils import PassThroughBuffer


class AgentMrMeeseeksToolManager(BaseToolManager):
    def __init__(
        self, agent_mr_meeseeks: AgentMrMeeseeks, logger: Optional[PassThroughBuffer] = None
    ):
        self.agent_mr_meeseeks = agent_mr_meeseeks
        self.logger = logger

    def build_tools(self) -> List[Tool]:
        tools = [
            Tool(
                name="mr-meeseeks-task",
                func=lambda: self.agent_mr_meeseeks.run(),
                description="Exposes the run command of the AgentMrMeeseeks class, which runs the task and reports the tool outputs back to the master.",
                example="mr-meeseeks-task",
                return_direct=True,
                verbose=True,
            )
        ]
        return tools
