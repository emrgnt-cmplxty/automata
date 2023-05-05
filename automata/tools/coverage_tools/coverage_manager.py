from automata.core.base.base_selector import BaseSelector
from automata.tools.coverage_tools.coverage_generator import CoverageGenerator


class CoverageManager(BaseSelector):
    def __init__(self, write=False, num_items_to_show=10):
        self.coverage_generator = CoverageGenerator()
        if write:
            self.coverage_generator.write_coverage_xml()
        coverage_df = self.coverage_generator.parse_coverage_xml()
        iterable = [(i, row.to_dict()) for i, row in coverage_df.iterrows()]
        super().__init__(iterable, num_items_to_show)

    def process_item(self, item):
        module_path = item["module"]
        function_name = item["object"]
        uncovered_line_numbers = sorted(item["line_number"])
        breakpoint()
        lines = self.coverage_generator.indexer.retrieve_outer_code_by_line(
            module_path, uncovered_line_numbers[-1]
        )
        breakpoint()
        # marked_lines = []
        # for line in lines:
        #     if uncovered_line_numbers:
        #         if line.startswith(str(uncovered_line_numbers[0])):
        #             line = f"{line}    <---"
        #             uncovered_line_numbers.pop(0)
        #     marked_lines.append(line[:])
        #
        # marked_code = '\n'.join(marked_lines)

        output = f"""
Write a test to satisfy the following coverage gap:\n\n
Module: {module_path}\n\n
Function: {function_name}\n\n
Uncovered lines: {uncovered_line_numbers}\n\n
Code:
```
{lines}
```
        """

        return output


if __name__ == "__main__":
    coverage_manager = CoverageManager(write=False)
    breakpoint()
    print(coverage_manager.list_items())
    breakpoint()
    print(coverage_manager.select_and_process_item(3))
