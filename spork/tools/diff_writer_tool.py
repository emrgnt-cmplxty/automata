from langchain import LLMChain, PromptTemplate
from langchain.agents import Tool
from langchain.llms import BaseLLM

example = """I have a file setup.py and I need to change it so in the beginning it prints out hello world\n
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


class DiffWriterTool(Tool):
    def __init__(self, llm: BaseLLM):
        diff_prompt = PromptTemplate(
            input_variables=["question"], template=DIFF_PROMPT_TEMPLATE + "Q: {question}"
        )
        diff_writing_chain = LLMChain(llm=llm, prompt=diff_prompt)
        super().__init__(
            name="Diff writer tool",
            func=diff_writing_chain.run,
            description=f"Useful for converting instructions to edit a file into a diff that can be applied to the file to effect the changes."
            f"Example: {example}",
        )
