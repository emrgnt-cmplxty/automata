from typing import List

from spork.core.base.tool import Tool

from .base_tool_manager import BaseToolManager


def build_tools(tool_manager: BaseToolManager) -> List[Tool]:
    """Build tools from a tool manager."""
    return tool_manager.build_tools()


def build_tools_with_meeseeks(tool_manager: BaseToolManager) -> List[Tool]:
    """Build tools from a tool manager with meeseeks."""
    return tool_manager.build_tools_with_meeseeks()
