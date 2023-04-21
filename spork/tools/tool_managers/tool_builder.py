from typing import List

from spork.tools import Tool

from .base_tool_manager import BaseToolManager


def build_tools(tool_manager: BaseToolManager) -> List[Tool]:
    return tool_manager.build_tools()


def build_tools_with_meeseeks(tool_manager: BaseToolManager) -> List[Tool]:
    return tool_manager.build_tools_with_meeseeks()
