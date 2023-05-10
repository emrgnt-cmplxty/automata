import logging
import os
import subprocess
import xml.etree.ElementTree as ET

import pandas as pd

from automata.config import REPOSITORY_PATH
from automata.tools.python_tools.python_indexer import PythonIndexer

logger = logging.getLogger(__name__)


class CoverageAnalyzer:
    """
    A class to produce a coverage report, load it and parse it into a dataframe.
    The df is generated so the info could be consumed by python indexer.
    # TODO: The nested definitions are not super consistently handled but the indexer should be robust against that given good naming
    # TODO: this is pretty slow
    """

    ROOT_DIR = REPOSITORY_PATH
    ROOT_MODULE = "automata"
    DIR_TO_INDEX = os.path.join(ROOT_DIR, ROOT_MODULE)
    COVERAGE_FILE_NAME = "coverage_analyzer_report.xml"
    COVERAGE_FILE_PATH = os.path.join(ROOT_DIR, COVERAGE_FILE_NAME)

    def __init__(self):
        self.indexer = PythonIndexer(self.DIR_TO_INDEX)

    def write_coverage_xml(self, force=False):
        """
        Writes a coverage report to the coverage.xml file
        """
        logger.debug("Writing coverage data...")
        if force or not os.path.exists(self.COVERAGE_FILE_PATH):
            subprocess.run(
                [
                    "pytest",
                    "-n",
                    "4",
                    f"--cov={self.ROOT_MODULE}",
                    f"--cov-report=xml:{self.COVERAGE_FILE_NAME}",
                ],
                cwd=self.ROOT_DIR,
                stdout=subprocess.DEVNULL,  # suppress output
            )
        logger.debug("Done writing coverage data.")

    def parse_coverage_xml(self):
        logger.debug("Parsing coverage data...")
        tree = ET.parse(self.COVERAGE_FILE_PATH)
        root = tree.getroot()

        data = []
        for package in root.findall(".//package"):
            package_name = package.get("name")
            if package_name.startswith("automata."):
                package_name = package_name[9:]
            for cls in package.findall(".//class"):
                class_name = cls.get("name")  # not a real class name, merely the name of the file
                for line in cls.findall(".//line"):
                    line_data = {
                        "module": f"{package_name}.{class_name[:-3]}",  # see above, remove .py
                        "line_number": int(line.get("number")),
                        "hits": int(line.get("hits")),
                    }
                    data.append(line_data)
        df = pd.DataFrame(data)
        uncovered_lines = df[df["hits"] == 0]
        uncovered_lines["object"] = uncovered_lines.apply(
            lambda x: self._function_name_from_row(x), axis=1
        )
        uncovered_lines = uncovered_lines[
            uncovered_lines["object"] != self.indexer.NO_RESULT_FOUND_STR
        ]

        uncovered_lines = (
            uncovered_lines.groupby(["module", "object"]).agg({"line_number": list}).reset_index()
        )
        uncovered_lines["percent_covered"] = uncovered_lines.apply(
            lambda x: self._percent_covered_function_from_row(x), axis=1
        )
        # sort by percent covered ascending
        uncovered_lines = uncovered_lines.sort_values(
            by=["percent_covered"], ascending=True
        ).reset_index(drop=True)

        logger.debug("Coverage data parsed.")
        return uncovered_lines

    def _function_name_from_row(self, row) -> str:
        """
        Helper function to retrieve the function name from metadata in the row of a dataframe
        :param row: A row of a dataframe that has package, module and line number entries
        see TODO in class docstring
        """
        name = self.indexer.retrieve_parent_function_name_by_line(row.module, row.line_number)
        return name

    def _percent_covered_function_from_row(self, row):
        """
        Helper function to retrieve the percent covered from metadata in the row of a dataframe
        :param row:
        see TODO in class docstring
        """
        start, end = self.indexer.retrieve_parent_function_node_lines(
            row.module, row.line_number[0]
        )
        num_uncovered = len(row.line_number)
        num_total = end - start + 1  # to account for inclusivity
        percent_covered = 1 - (num_uncovered / num_total)
        return percent_covered

    def clean_up(self):
        """
        Removes the coverage.xml file
        """
        os.remove(self.COVERAGE_FILE_PATH)


if __name__ == "__main__":
    coverage_generator = CoverageAnalyzer()
    coverage_generator.write_coverage_xml()
    df = coverage_generator.parse_coverage_xml()
    print(df.list_next_items())
    coverage_generator.clean_up()
