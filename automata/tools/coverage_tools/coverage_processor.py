import logging
from functools import lru_cache

import pandas as pd

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

    def __init__(self, coverage_analyzer, do_create_issue=False):
        self.coverage_analyzer = coverage_analyzer
        self.do_create_issue = do_create_issue

    @lru_cache(maxsize=5)
    def get_coverage_df(self, module_path: str) -> pd.DataFrame:
        self.coverage_analyzer.write_coverage_xml(module_path)
        coverage_df = self.coverage_analyzer.parse_coverage_xml()
        return coverage_df

    def list_coverage_gaps(self, module_path: str) -> str:
        coverage_df = self.get_coverage_df(module_path)
        coverage_df = coverage_df[["module", "object", "percent_covered"]]
        return coverage_df.to_string()

    def process_coverage_gap(self, module: str, object: str):
        module_path = module
        function_name = object
        coverage_df = self.get_coverage_df(module_path)
        # get lines from df by module and object
        uncovered_line_numbers = sorted(
            coverage_df[
                (coverage_df["module"] == module_path) & (coverage_df["object"] == function_name)
            ]["line_number"].iloc[0]
        )

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


# TODO: remove and write tests in separate file
if __name__ == "__main__":
    coverage_analyzer = CoverageAnalyzer()
    coverage_manager = CoverageProcessor(coverage_analyzer)
    print(coverage_manager.list_coverage_gaps("tools.python_tools.python_indexer"))
    coverage_manager.process_coverage_gap(
        "tools.python_tools.python_indexer",
        "retrieve_parent_function_name_by_line",
    )
