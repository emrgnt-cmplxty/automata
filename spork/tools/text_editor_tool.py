import os
from io import StringIO

from diff_match_patch import diff_match_patch
from langchain import LLMChain, PromptTemplate
from langchain.agents import Tool
from langchain.llms import BaseLLM
from unidiff import PatchSet

example = """Instructions: I have a file setup.py and I need to change it so in the beginning it prints out hello world\n
                    Context: I have a file /home/users/user/proj/proj1/setup.py with the following contents at
                    1: from setuptools import find_packages, setup
                    2:
                    3: def read_requirements():
                    4:     with open(\"requirements.txt\", \"r\") as req_file:
                    5:         return req_file.readlines()
                    6:
                    7:
                    \n
                    --- home/users/user/proj/proj1/setup.py
                    +++ home/users/user/proj/proj1/setup.py
                    @@ -1,5 +1,7 @@
                     from setuptools import find_packages, setup
                    +print(\"Hello, world!\")
                    +
                     def read_requirements():
                         with open(\"requirements.txt\", \"r\") as req_file:
                             return req_file.readlines()


                    """

DIFF_PROMPT_TEMPLATE = (
    f"You are an expert diff writer. Your job is to take instructions to edit a file, with relevant context,"
    f"and produce a diff "
    f"that can be applied to the file to effect the changes. Make sure to use the full paths.\n\n"
    f"Example:"
    f"{example}\n\n"
    f"You should write the diff and diff only. Do not include the instructions or context or any other thoughts."
    f"\n\n"
)


class TextEditorTool(Tool):
    def __init__(self, llm: BaseLLM, codebase_oracle_tool: Tool):
        diff_prompt = PromptTemplate(
            input_variables=["question"], template=DIFF_PROMPT_TEMPLATE + "Q: {question}"
        )
        diff_writing_chain = LLMChain(llm=llm, prompt=diff_prompt)
        super().__init__(
            name="Text editor tool",
            func=lambda x: self.edit(x, diff_writing_chain, codebase_oracle_tool),
            description="A tool to edit text files.",
        )

    def edit(
        self, instructions: str, diff_writing_chain: LLMChain, codebase_oracle_tool: Tool
    ) -> str:
        context_prompt = (
            f"What are the relevant file contents that a developer might need to follow these instructions? "
            f"Provide raw content without changing it.\n\n"
            f"Instructions: {instructions}"
        )
        context = codebase_oracle_tool.run(context_prompt).strip()

        print(context)
        breakpoint()
        diff_query = f"Instructions: {instructions}\n\n Context: {context}\n\n Begin!"

        diff = diff_writing_chain.run(diff_query)
        breakpoint()
        try:
            return self.apply_diff(diff)
        except Exception as e:
            return f"Error applying diff: {e}"

    def apply_diff(self, diff_string: str) -> str:
        patch_set = PatchSet(StringIO(diff_string))
        dmp = diff_match_patch()
        original_file_path = patch_set[0].source_file
        print("=====================================")
        print(patch_set)
        if not os.path.exists(original_file_path):
            return f"File not found: {original_file_path}"

        with open(original_file_path, "r") as file:
            original_file_content = file.read()

        new_file_content = original_file_content
        patch_dmp = dmp.patch_fromText(str(patch_set))

        new_file_content = dmp.patch_apply(patch_dmp, new_file_content)[0]

        with open(original_file_path, "w") as file:
            file.write(new_file_content)
        return "Diff applied successfully"
