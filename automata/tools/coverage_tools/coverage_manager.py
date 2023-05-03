import os
import subprocess
import xml.etree.ElementTree as ET
from _ast import AsyncFunctionDef, ClassDef, FunctionDef
from typing import List, Union

import pandas as pd

from automata.config import REPOSITORY_PATH
from automata.tools.python_tools.python_indexer import PythonIndexer


class CoverageManager:
    """
    A class to produce a coverage report, load it and parse it into memory
    # TODO: right now this only supports functions and methods.
    # TODO: It doesn't handle nested definitions (besides class.method) well.
    """

    ROOT_DIR = REPOSITORY_PATH
    ROOT_MODULE = "automata"
    DIR_TO_INDEX = os.path.join(ROOT_DIR, ROOT_MODULE)
    COVERAGE_FILE_NAME = "coverage.xml"
    COVERAGE_FILE_PATH = os.path.join(ROOT_DIR, COVERAGE_FILE_NAME)

    def __init__(self):
        self.indexer = PythonIndexer(self.DIR_TO_INDEX)

    def write_coverage_xml(self):
        """
        Writes a coverage report to the coverage.xml file
        """
        subprocess.run(
            [
                "coverage",
                "run",
                f"--source={self.ROOT_MODULE}",
                "-m",
                "pytest",
            ],
            cwd=self.ROOT_DIR,
            check=True,
        )
        subprocess.run(
            ["coverage", "xml"],
            cwd=self.ROOT_DIR,
            check=True,
        )

    def parse_coverage_xml(self):
        tree = ET.parse(self.COVERAGE_FILE_PATH)
        root = tree.getroot()

        data = []
        for package in root.findall(".//package"):
            package_name = package.get("name")
            if package_name.startswith("automata."):
                package_name = package_name[9:]
            for cls in package.findall(".//class"):
                class_name = cls.get("name")
                for line in cls.findall(".//line"):
                    line_data = {
                        "module": f"{package_name}.{class_name[:-3]}",
                        "line_number": int(line.get("number")),
                        "hits": int(line.get("hits")),
                    }
                    data.append(line_data)
        df = pd.DataFrame(data)
        uncovered_lines = df[df["hits"] == 0]
        uncovered_lines["object"] = uncovered_lines.apply(
            lambda x: self._object_name_from_row(x), axis=1
        )
        uncovered_lines = uncovered_lines[uncovered_lines["object"] != "None"]

        uncovered_lines = (
            uncovered_lines.groupby(["module", "object"]).agg({"line_number": list}).reset_index()
        )
        uncovered_lines["percent_covered"] = uncovered_lines.apply(
            lambda x: self._percent_covered_function_from_row(x), axis=1
        )
        # sort by percent covered ascending
        uncovered_lines = uncovered_lines.sort_values(by=["percent_covered"], ascending=True)
        breakpoint()
        return uncovered_lines

    def _get_nodes_from_row(self, row) -> List[Union[ClassDef, FunctionDef, AsyncFunctionDef]]:
        line_number = row.line_number[0] if isinstance(row.line_number, list) else row.line_number
        return self.indexer.retrieve_nodes_by_line(row.module, line_number)

    def _object_name_from_row(self, row) -> str:
        """
        Helper function to retrieve the function name from metadata in the row of a dataframe
        :param row: A row of a dataframe that has package, module and line number entries
        see TODO in class docstring
        """
        nodes = self._get_nodes_from_row(row)
        class_nodes = [node for node in nodes if isinstance(node, ClassDef)]
        function_nodes = [
            node for node in nodes if isinstance(node, (FunctionDef, AsyncFunctionDef))
        ]
        name = ""
        if function_nodes:
            node = function_nodes[0]
            name = node.name
            if class_nodes:
                name = f"{class_nodes[0].name}.{name}"

        return name or "None"

    def _percent_covered_function_from_row(self, row):
        """
        Helper function to retrieve the percent covered from metadata in the row of a dataframe
        :param row:
        see TODO in class docstring
        """
        nodes = self._get_nodes_from_row(row)
        function_nodes = [
            node for node in nodes if isinstance(node, (FunctionDef, AsyncFunctionDef))
        ]
        class_nodes = [node for node in nodes if isinstance(node, ClassDef)]
        if function_nodes:
            node = function_nodes[0]
        elif class_nodes:
            node = class_nodes[0]

        num_uncovered = len(row.line_number)
        num_total = node.end_lineno - node.lineno + 1  # to account for inclusivity
        percent_covered = 1 - (num_uncovered / num_total)
        return percent_covered


if __name__ == "__main__":
    cm = CoverageManager()
    cm.write_coverage_xml()
    cm.parse_coverage_xml()
