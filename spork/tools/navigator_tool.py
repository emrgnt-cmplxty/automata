from langchain import LLMBashChain, PALChain
from langchain.agents import Tool
from langchain.llms import BaseLLM

# flake8: noqa
from langchain.prompts.prompt import PromptTemplate

template = (
    """
    # Generate Python3 Code to manipulate files and directories
    # Q: Change the current working directory to: /home/username/Downloads
    import os
    os.chdir('/home/username/Downloads')
    
    # Q: List all files in the current directory
    import os
    current_directory = os.getcwd()
    os.listdir(current_directory)
    
    # Q: List all files in directory: /home/username/Documents
    import os
    os.listdir('/home/username/Documents')
    
    # Q: What directory am I in?
    import os
    os.getcwd()
    
    # Q: Make a new directory: /home/username/Documents/new_directory
    import os
    os.mkdir('/home/username/Documents/new_directory')
    
    # Q: Move a file myfile.txt to /home/username/Documents/ directory:
    import os
    os.rename('myfile.txt', '/home/username/Documents/myfile.txt')
    
    # Q: Move a directory: /home/username/Documents/new_directory to /home/username/Documents/new_directory2
    import os
    shutil.move('/home/username/Documents/new_directory', '/home/username/Documents/new_directory2')
    
    # Q: Copy a file myfile.txt to /home/username/Documents/ directory:
    import shutil
    shutil.copy('myfile.txt', '/home/username/Documents/myfile.txt')
    
    # Q: Delete a file myfile.txt
    import os
    os.remove('myfile.txt')
    
    # Q: Delete a directory: /home/username/Documents/new_directory
    import os
    os.rmdir('/home/username/Documents/new_directory')
    
    # Q: Delete a directory and all its contents: /home/username/Documents/new_directory
    import shutil
    shutil.rmtree('/home/username/Documents/new_directory')
    
    
    # Q: {question}
    """.strip()
    + "\n"
)

PROMPT = PromptTemplate(input_variables=["question"], template=template)


class LocalNavigatorTool(Tool):
    def __init__(self, llm: BaseLLM):
        chain = PALChain(prompt=PROMPT, llm=llm)

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
