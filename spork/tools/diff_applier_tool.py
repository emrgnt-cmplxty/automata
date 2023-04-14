from io import StringIO

from diff_match_patch import diff_match_patch
from langchain.agents import Tool
from unidiff import PatchSet


class DiffApplierTool(Tool):
    def __init__(self):
        super().__init__(
            name="diff_applier_tool",
            func=self.apply_diff,
            description="Apply a diff to the codebase using diff_match_patch. The input should be a perfectly formatted diff string and nothing else",
        )

    def apply_diff(self, diff_string: str) -> str:
        try:
            patch_set = PatchSet(StringIO(diff_string))
            dmp = diff_match_patch()
            original_file_path = patch_set[0].source_file

            with open(original_file_path, "r") as file:
                original_file_content = file.read()

            new_file_content = original_file_content
            patch_dmp = dmp.patch_fromText(str(patch_set))

            new_file_content = dmp.patch_apply(patch_dmp, new_file_content)[0]

            with open(original_file_path, "w") as file:
                file.write(new_file_content)
            return f"Success! Applied diff to file: {original_file_path}"
        except Exception as e:
            return f"Error: {e}"
