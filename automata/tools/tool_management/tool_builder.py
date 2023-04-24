from typing import List

from automata.core.base.tool import Tool

from .base_tool_manager import BaseToolManager


def build_tools(tool_manager: BaseToolManager) -> List[Tool]:
    """Build tools from a tool manager."""
    return tool_manager.build_tools()


def build_tools_with_automata(tool_manager: BaseToolManager) -> List[Tool]:
    """Build tools from a tool manager with automata."""
    return tool_manager.build_tools_with_automata()
