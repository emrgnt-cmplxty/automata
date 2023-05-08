from typing import List

from automata.core.base.tool import Tool
from automata.tool_management.base_tool_manager import BaseToolManager
from automata.tools.coverage_tools.coverage_processor import CoverageProcessor


class CoverageToolManager(BaseToolManager):
    def __init__(self):
        self.coverage_processor = CoverageProcessor(write_fresh_report=True)

    def _run_show_coverage_gaps(self, input_str):
        try:
            return self.coverage_processor.list_items()
        except Exception as e:
            return str(e)

    def _run_select_and_process_coverage_gap(self, index):
        try:
            return self.coverage_processor.select_and_process_item(int(index))
        except Exception as e:
            return str(e)

    def build_tools(self) -> List[Tool]:
        tools = [
            Tool(
                name="List coverage gaps",
                description="Useful for listing coverage gaps, a few at a time. Calling this repeatedly will yield the next gaps, until there are no more left, at which point the iteration resets. "
                "Returns a list of coverage gaps including the module, function, uncovered lines, and the overall covered percentage.",
                func=self._run_show_coverage_gaps,  # no input necessary
            ),
            Tool(
                name="Process coverage gap",
                description="Useful for creating the context needed to write a test to satisfy a coverage gap. Input should be the index of the coverage gap item. "
                "Returns relevant info, like the module, function, uncovered lines, and raw code with uncovered lines marked.",
                func=self._run_select_and_process_coverage_gap,
            ),
        ]
        return tools
