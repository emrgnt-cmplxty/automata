from automata.core.base.base_selector import BaseSelector
from automata.tools.coverage_tools.coverage_analyzer import CoverageAnalyzer


class CoverageProcessor(BaseSelector):
    def __init__(self, write_fresh_report=False, num_items_to_show=10):
        self.coverage_generator = CoverageAnalyzer()
        if write_fresh_report:
            self.coverage_generator.write_coverage_xml()
        coverage_df = self.coverage_generator.parse_coverage_xml()
        iterable = [(i, row.to_dict()) for i, row in coverage_df.iterrows()]
        super().__init__(iterable, num_items_to_show)

    def process_item(self, item):
        module_path = item["module"]
        function_name = item["object"]
        uncovered_line_numbers = sorted(item["line_number"])
        uncovered_line_numbers_queue = uncovered_line_numbers[:]

        lines = self.coverage_generator.indexer.retrieve_parent_code_by_line(
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

        output = (
            f"Write a test to satisfy the following coverage gap:\n"
            f"Module: {module_path}\n"
            f"Function: {function_name}\n"
            f"Uncovered lines: {uncovered_line_numbers}\n"
            f"Code:\n"
            f"```"
            f"{marked_code}"
            f"```"
        )

        return output


if __name__ == "__main__":
    coverage_manager = CoverageProcessor(write_fresh_report=True)
    print(coverage_manager.list_items())
    print(coverage_manager.select_and_process_item(0))
