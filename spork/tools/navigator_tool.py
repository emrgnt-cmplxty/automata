from langchain import LLMBashChain, PALChain
from langchain.agents import Tool
from langchain.llms import BaseLLM

# flake8: noqa
from langchain.prompts.prompt import PromptTemplate

template = (
    """
    # Generate Python3 Code to manipulate files and directories. 
    If you don't understand request, or it asks you to do something other than manipulate files and directories,
    say "Invalid request."
    # Q: Change the current working directory to: /home/username/Downloads
    import os
    answer = os.chdir('/home/username/Downloads')
    if answer is None: answer = "Success."
    
    # Q: List all files in the current directory
    import os
    current_directory = os.getcwd()
    answer = os.listdir(current_directory)
    
    # Q: List all files in directory: /home/username/Documents
    import os
    answer = os.listdir('/home/username/Documents')
    
    # Q: What directory am I in?
    import os
    answer = os.getcwd()
    
    # Q: Make a new directory: /home/username/Documents/new_directory
    import os
    answer = os.mkdir('/home/username/Documents/new_directory')
    if answer is None: answer = "Success."
    
    # Q: Move a file myfile.txt to /home/username/Documents/ directory:
    import os
    answer = os.rename('myfile.txt', '/home/username/Documents/myfile.txt')
    if answer is None: answer = "Success."
    
    # Q: Move a directory: /home/username/Documents/new_directory to /home/username/Documents/new_directory2
    import os
    answer = shutil.move('/home/username/Documents/new_directory', '/home/username/Documents/new_directory2')
    if answer is None: answer = "Success."
    
    # Q: Copy a file myfile.txt to /home/username/Documents/ directory:
    import shutil
    answer = shutil.copy('myfile.txt', '/home/username/Documents/myfile.txt')
    if answer is None: answer = "Success."
    
    # Q: Delete a file myfile.txt
    import os
    answer = os.remove('myfile.txt')
    if answer is None: answer = "Success."
    
    # Q: Delete a directory: /home/username/Documents/new_directory
    import os
    answer = os.rmdir('/home/username/Documents/new_directory')
    if answer is None: answer = "Success."
    
    # Q: Delete a directory and all its contents: /home/username/Documents/new_directory
    import shutil
    answer = shutil.rmtree('/home/username/Documents/new_directory')
    if answer is None: answer = "Success."
    
    # Q: What is 2 + 2?
    answer = "Invalid request."
    
    # Q: Write a function to compute the Nth Fibonacci number.
    answer = "Invalid request."
    
    # Q: {question}
    """.strip()
    + "\n"
)

PROMPT = PromptTemplate(input_variables=["question"], template=template)


class LocalNavigatorTool(Tool):
    def __init__(self, llm: BaseLLM):
        chain = PALChain(prompt=PROMPT, llm=llm, get_answer_expr="print(answer)")

        super().__init__(
            name="Local navigator tool",
            func=lambda q: chain.run(q),
            description="Useful for when you need to manipulate directories and files locally. "
            "It doesn't know what you're working on, but it knows how to take you around the machine you're on. "
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
