from langchain import LLMBashChain
from langchain.agents import Tool
from langchain.llms import BaseLLM
from langchain.prompts.prompt import PromptTemplate

_PROMPT_TEMPLATE = """If someone asks you to perform a task, your job is to come up with a series of bash commands that will perform the task. There is no need to put "#!/bin/bash" in your answer. Make sure to reason step by step, using this format:
Question: "copy the files in the directory named 'target' into a new directory at the same level as target called 'myNewDirectory'"
I need to take the following actions:
- List all files in the directory
- Create a new directory
- Copy the files from the first directory into the second directory
```bash
ls
mkdir myNewDirectory
cp -r target/* myNewDirectory
```

Do not use 'echo' when writing the script. Do not put anything after the command and set of triple backticks

That is the format you *must* follow. Begin!
Question: {question}"""

PROMPT = PromptTemplate(input_variables=["question"], template=_PROMPT_TEMPLATE)


class LocalNavigatorTool(Tool):
    def __init__(self, llm: BaseLLM):
        chain = LLMBashChain(llm=llm, prompt=PROMPT, verbose=False)

        super().__init__(
            name="Local navigator tool",
            func=lambda q: chain.run(q),
            description="Useful for when you need to manipulate directories and files locally. "
            "It doesn't know what you're working on, but it knows how to take you around the machine you're on."
            "Input should be a single fully formed request. "
            "Examples of what to ask: "
            "What directory am I in? "
            "What are the contents of the current directory? "
            "Give me all python files in this directory: directory_path. "
            "Go to this directory: directory_path."
            "Make a new directory: directory_path/directory_name. "
            "Make a new file: directory_path/file_name. "
            "Copy this file: file_path to this directory: directory_path. ",
        )
