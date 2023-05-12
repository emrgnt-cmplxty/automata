import logging
from typing import Any

from automata.config import GITHUB_API_KEY, REPOSITORY_NAME
from automata.core.base.github_manager import GitHubManager
from automata.tools.coverage_tools.coverage_analyzer import CoverageAnalyzer

logger = logging.getLogger(__name__)


class CoverageProcessor:
    """
    CoverageProcessor uses a CoverageAnalyzer to process coverage gaps, show them to the user and selectively create issues for them
    TODO: this is pretty slow with parsing, maybe we can cache the coverage_df and only re-parse when we need to
    TODO: coverage report is being "cached" right now but it would be nice to clean it up when the user is done, or make the agent more stateful
    """

    def __init__(self, coverage_analyzer, do_create_issue=False, num_items_to_show=10):
        self.coverage_analyzer = coverage_analyzer
        self.do_create_issue = do_create_issue
        self.num_items_to_show = num_items_to_show
        # lazy fields
        self.coverage_df = None
        self.item_iterable = []
        self._item_iterator = None

    def _refresh(self):
        if self.coverage_df is None:
            self.coverage_analyzer.write_coverage_xml()
            self.coverage_df = self.coverage_analyzer.parse_coverage_xml()
            self.item_iterable = [(i, row.to_dict()) for i, row in self.coverage_df.iterrows()]

    @property
    def item_iterator(self):
        if not self._item_iterator:
            self._item_iterator = iter(self.item_iterable)
        return self._item_iterator

    def list_next_items(self) -> str:
        self._refresh()
        items = []
        for i in range(self.num_items_to_show):
            index, item = next(self.item_iterator)
            items.append(f"{index}. {item}")
        return "\n".join(items)

    def select_and_process_item(self, index) -> Any:
        self._refresh()
        logger.debug(f"Processing coverage data {index}...")
        if index not in range(len(self.item_iterable)):
            raise ValueError(f"Index {index} not in coverage dataframe")
        return self._process_item(self.item_iterable[index][1])

    def _process_item(self, item):
        module_path = item["module"]
        function_name = item["object"]
        uncovered_line_numbers = sorted(item["line_number"])
        uncovered_line_numbers_queue = uncovered_line_numbers[:]

        lines = self.coverage_analyzer.indexer.retrieve_parent_code_by_line(
            module_path, uncovered_line_numbers[0], True
        ).splitlines()
        marked_lines = []
        for line in lines:
            if uncovered_line_numbers_queue and line.startswith(
                str(uncovered_line_numbers_queue[0])
            ):
                marked_lines.append(f"*** {line}")
                uncovered_line_numbers_queue.pop(0)
            else:
                marked_lines.append(line)
        marked_code = "\n".join(marked_lines)

        issue_body = (
            f"Write a test to satisfy the following coverage gap:\n"
            f"Module: {module_path}\n"
            f"Function: {function_name}\n"
            f"Uncovered lines: {uncovered_line_numbers}\n"
            f"Code:\n"
            f"```"
            f"{marked_code}"
            f"```"
        )
        issue_title = f"Test coverage gap: {module_path} - {function_name}"
        if self.do_create_issue:
            GitHubManager(access_token=GITHUB_API_KEY, remote_name=REPOSITORY_NAME).create_issue(
                issue_title, issue_body, ["test-coverage-gap"]
            )
        return f"Processed - {issue_title}"


if __name__ == "__main__":
    coverage_analyzer = CoverageAnalyzer()
    coverage_manager = CoverageProcessor(coverage_analyzer)

    print(coverage_manager.list_next_items())
    print(coverage_manager.select_and_process_item(0))
    coverage_analyzer.clean_up()
