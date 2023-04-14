import os
from io import StringIO

from langchain import LLMChain
from langchain.agents import Tool
from langchain.llms import BaseLLM
from unidiff import PatchSet


class TextEditorTool(Tool):
    def __init__(self, llm: BaseLLM, codebase_oracle_tool: Tool):
        self.llm = llm
        super().__init__(
            name="Text editor tool",
            func=lambda x: self.edit(x, codebase_oracle_tool),
            description="A tool to edit text files.",
        )

    def edit(self, instructions: str, codebase_oracle_tool: Tool) -> str:
        filename_prompt = (
            f"The following instructions contain a filename. Please give me the filename with full path."
            f"For example:\n\n"
            f"Instructions: 'Add the line to print hello world in main.py '\n"
            f"/home/user/proj/project1/main.py "
            f"\n\n"
            f"Begin!"
            f"Instructions: {instructions}\n"
        )
        filename = codebase_oracle_tool.run(filename_prompt).strip()

        if not os.path.exists(filename):
            return f"File not found: {filename}"

        context_prompt = (
            f"What are the relevant code snippets for the following changes? "
            f"Provide raw code.\n\n"
            f"Filename: {filename}\n\n"
            f"Instructions: {instructions}\n\n"
            f"Return the results only.\n\n"
            f"Begin!"
        )
        context = codebase_oracle_tool.run(context_prompt).strip()

        example = """Instructions: I have a file setup.py and I need to change it so in the beginning it prints out hello world\n
                    Context: I have a file main.py with the following contents
                    from setuptools import find_packages, setup

                    def read_requirements():
                        with open("requirements.txt", "r") as req_file:
                            return req_file.readlines()


                    setup(
                        name="improved-spork",
                        version="0.1.0",
                        packages=find_packages(),
                        install_requires=read_requirements(),
                        entry_points={
                            "console_scripts": [
                                # If you want to create command-line executables, you can define them here.
                                # e.g.: 'my-command=your_project_name.framework.main:main',
                            ],
                        },
                        python_requires=">=3.9",  # Adjust this to your desired minimum Python version
                    )
                    \n
                    --- a/setup.py
                    +++ b/setup.py
                    @@ -1,5 +1,7 @@
                     from setuptools import find_packages, setup
                    +print("Hello, world!")
                    +
                     def read_requirements():
                         with open("requirements.txt", "r") as req_file:
                             return req_file.readlines()
                    """

        diff_prompt = (
            f"You are an expert diff writer. Your job is to take instructions to edit a file, with relevant context,"
            f"and produce a diff "
            f"that can be applied to the file to effect the changes.\n\n"
            f"Example:"
            f"{example}\n\n"
            f"You should write the diff and diff only. Do not include the instructions or context or any other thoughts.\n\n"
        )

        diff_query = f"Instructions: {instructions}\n\n Context: {context}\n\n Begin!"

        diff_writing_chain = LLMChain(llm=self.llm, prompt=diff_prompt)
        diff = diff_writing_chain.run(diff_query).strip()
        try:
            return self.apply_diff(diff)
        except Exception as e:
            return f"Error applying diff: {e}"

    def apply_diff(self, diff_string: str) -> str:
        patch_set = PatchSet(StringIO(diff_string))
        for patch in patch_set:
            original_file_path = patch.source_file
            if not os.path.exists(original_file_path):
                return f"File not found: {original_file_path}"

            with open(original_file_path, "r") as file:
                original_file_content = file.read()

            new_file_content = original_file_content
            for hunk in patch:
                new_file_content = hunk.apply_to(new_file_content, inplace=True)

            with open(original_file_path, "w") as file:
                file.write(new_file_content)
        return "Diff applied successfully"
