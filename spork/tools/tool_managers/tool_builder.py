from typing import List, Optional

from langchain.agents import Tool

from spork.tools.utils import PassThroughBuffer

from .base_tool_manager import BaseToolManager


def build_tools(
    tool_manager: BaseToolManager, logger: Optional[PassThroughBuffer] = None
) -> List[Tool]:
    return tool_manager.build_tools()
