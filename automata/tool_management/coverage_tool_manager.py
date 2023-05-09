from typing import List

from automata.core.base.tool import Tool
from automata.tool_management.base_tool_manager import BaseToolManager
from automata.tools.coverage_tools.coverage_analyzer import CoverageAnalyzer
from automata.tools.coverage_tools.coverage_processor import CoverageProcessor


class CoverageToolManager(BaseToolManager):
    def __init__(self, **kwargs):
        coverage_analyzer = CoverageAnalyzer()
        self.coverage_processor = CoverageProcessor(coverage_analyzer, do_create_issue=True)
        self.model = kwargs.get("model") or "gpt-4"
        self.temperature = kwargs.get("temperature") or 0.7
        self.verbose = kwargs.get("verbose") or False
        self.stream = kwargs.get("stream") or True

    def _run_show_coverage_gaps(self, input_tuple):
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
                name="list-coverage-gaps",
                description="Useful for listing coverage gaps, a few at a time. Calling this repeatedly will yield the next gaps, until there are no more left, at which point the iteration resets. "
                "Returns a list of coverage gaps including the module, function, uncovered lines, and the overall covered percentage.",
                func=self._run_show_coverage_gaps,  # no input necessary
                return_direct=True,
            ),
            Tool(
                name="process-coverage-gap",
                description="Useful for creating the context needed to write a test to satisfy a coverage gap. Input should be the index of the coverage gap item. "
                "Returns relevant info, like the module, function, uncovered lines, and raw code with uncovered lines marked.",
                func=lambda module_object_tuple: self._run_select_and_process_coverage_gap(
                    *module_object_tuple
                ),
            ),
        ]
        return tools
