from typing import List

from langchain.agents import Tool

from .base_tool_manager import BaseToolManager


def build_tools(tool_manager: BaseToolManager) -> List[Tool]:
    return tool_manager.build_tools()
