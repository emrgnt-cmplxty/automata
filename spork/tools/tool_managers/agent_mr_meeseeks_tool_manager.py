from typing import List, Optional

from spork.tools.agents.agent_mr_meeseeks import AgentMrMeeseeks
from spork.tools.tool import Tool
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
                name="python-agent-python-task",
                func=lambda: self.agent_mr_meeseeks.iter_task(),
                description="Exposes the iter_task command of the AgentMrMeeseeks class, which runs the task and reports the tool outputs back to the master.",
                example="python-agent-python-task",
                return_direct=True,
                verbose=True,
            )
        ]
        return tools
