from langchain import LLMChain, PromptTemplate
from langchain.agents import Tool
from langchain.llms import BaseLLM
from langchain.memory import ReadOnlySharedMemory

example = """I have a file setup.py and I need to change it so in the beginning it prints out hello world\n
            0: import os
            1: from setuptools import find_packages, setup
            2:
            3: def read_requirements():
            4:     with open(\"requirements.txt\", \"r\") as req_file:
            5:         return req_file.readlines()
            6:
            7:
            \n
            begin;
            open`home/users/user/proj/proj1/setup.py;
            insert`1`print(\"hello world\");
            end;
            \n\n
            I have a file myrepo/conf.json and I need to change the port to 8008\n
            16:    \"app_name\": \"myapp\",
            17:    \"version\": \"0.1.0\",
            18:    \"port\": 8000,
            \n
            begin;
            open`home/users/user/dev/myrepo/conf.json;
            replace`18`   \"port\": 8000,;
            end;
            """

PROMPT_TEMPLATE = (
    f"You are compiler. Your job is to take instructions to edit a file and convert them into line by line editing commands. "
    f"The only operations you support are open, insert, delete, and replace. Each of these operate on a whole line level. "
    f"You start every program with begin; command, followed by an open command, "
    f" followed by a series of insert, delete, and replace commands, finally followed by an end; command. "
    f"Valid state transitions are begin -> open -> insert, delete, replace -> end. "
    f"Here's how you open: open`FILE_PATH;"
    f"Here's how you insert: insert`LINE_NUMBER`TEXT_TO_INSERT;"
    f"Here's how you delete: delete`LINE_NUMBER;"
    f"Here's how you replace: replace`LINE_NUMBER`TEXT_TO_REPLACE;"
    f"Example:"
    f"{example}\n\n"
    f"Remember that inserts and deletes alter the line numbers of the surrounding lines, "
    f"specifically inserting a line will shift all lines below it down by one,"
    f"and deleting a line will shift all lines below it up by one. "
    f"Each instruction line number argument should account for the edits that will have occurred by then. "
    f"Do not deviate from this format and output the command sequence only."
    f"\n\n"
)


class EditInstructionsCompilerTool(Tool):
    def __init__(self, llm: BaseLLM, memory: ReadOnlySharedMemory):
        prompt = PromptTemplate(
            input_variables=["question"], template=PROMPT_TEMPLATE + "Q: {question}"
        )
        compiler_chain = LLMChain(llm=llm, prompt=prompt, memory=memory)
        super().__init__(
            name="Edit Instructions Compiler Tool",
            func=compiler_chain.run,
            description=f"Useful for compiling instructions into step-by-step commands for the editor. "
            f"Before using this tool, you *MUST* ask codebase oracle for the relevant context. Provide the full context as your input, do not shorten it. "
            f"Example: {example}",
        )
