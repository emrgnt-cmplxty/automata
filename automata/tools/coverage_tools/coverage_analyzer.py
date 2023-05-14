import logging
import os
import subprocess
import xml.etree.ElementTree as ET
from typing import cast

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
    COVERAGE_FILE_NAME = ".coverage_analyzer_report.xml"
    COVERAGE_FILE_PATH = os.path.join(ROOT_DIR, COVERAGE_FILE_NAME)

    def __init__(self):
        self.indexer = PythonIndexer(self.DIR_TO_INDEX)

    def write_coverage_xml(self, module_path: str):
        """
        Writes a coverage report to the coverage.xml file
        """
        logger.debug("Writing coverage data...")
        subprocess.run(
            [
                "coverage",
                "run",
                "--source",
                self.ROOT_MODULE,
                "-m",
                "pytest",
            ],
            cwd=self.ROOT_DIR,
            # stdout=subprocess.DEVNULL,
        )

        # check if path is a filesytem path or a module path
        if not os.path.exists(module_path):
            if "." in module_path and not module_path.endswith(".py"):
                module_path = module_path.replace(".", "/") + ".py"
            if not module_path.startswith(self.ROOT_MODULE):
                module_path = self.ROOT_MODULE + "/" + module_path
            module_path = os.path.join(self.ROOT_DIR, module_path)

        assert os.path.exists(module_path), f"Module path {module_path} does not exist"
        subprocess.run(
            [
                "coverage",
                "xml",
                "-o",
                self.COVERAGE_FILE_PATH,
                module_path,
            ],
            cwd=self.ROOT_DIR,
            # stdout=subprocess.DEVNULL,
        )

        logger.debug("Done writing coverage data.")

    def parse_coverage_xml(self) -> pd.DataFrame:
        logger.debug("Parsing coverage data...")
        tree = ET.parse(self.COVERAGE_FILE_PATH)
        root = tree.getroot()

        data = []
        for package in root.findall(".//package"):
            package_name = cast(str, package.get("name"))
            if package_name.startswith("automata."):
                package_name = package_name[9:]
            for cls in package.findall(".//class"):
                class_name = cast(
                    str, cls.get("name")
                )  # not a real class name, merely the name of the file
                for line in cls.findall(".//line"):
                    line_data = {
                        "module": f"{package_name}.{class_name[:-3]}",  # see above, remove .py
                        "line_number": int(cast(str, line.get("number"))),
                        "hits": int(cast(str, line.get("hits"))),
                    }
                    data.append(line_data)
        df = pd.DataFrame(data)
        df_uncovered_lines = df[df["hits"] == 0]
        df_uncovered_lines["object"] = df_uncovered_lines.apply(
            lambda x: self._function_name_from_row(x), axis=1
        )
        df_uncovered_lines = df_uncovered_lines[
            df_uncovered_lines["object"] != self.indexer.NO_RESULT_FOUND_STR
        ]

        df_uncovered_lines = (
            df_uncovered_lines.groupby(["module", "object"])
            .agg({"line_number": list})
            .reset_index()
        )
        df_uncovered_lines["percent_covered"] = df_uncovered_lines.apply(
            lambda x: self._percent_covered_function_from_row(x), axis=1
        )
        # sort by percent covered ascending
        df_uncovered_lines = df_uncovered_lines.sort_values(
            by=["percent_covered"], ascending=True
        ).reset_index(drop=True)

        logger.debug("Coverage data parsed.")

        return df_uncovered_lines

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
        TODO: the lines include the function signature, so the percent covered is not completely accurate
        """
        num_total = self.indexer.retrieve_parent_function_num_code_lines(
            row.module, row.line_number[0]
        )
        num_uncovered = len(row.line_number)
        percent_covered = 1 - (num_uncovered / num_total)
        return percent_covered

    def clean_up(self):
        """
        Removes the coverage.xml file
        """
        os.remove(self.COVERAGE_FILE_PATH)


# TODO: remove and write tests in separate file
if __name__ == "__main__":
    coverage_generator = CoverageAnalyzer()
    coverage_generator.write_coverage_xml("automata.tools.python_tools.python_indexer")
    df = coverage_generator.parse_coverage_xml()
    coverage_generator.clean_up()
