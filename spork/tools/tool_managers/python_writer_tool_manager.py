from typing import List

from langchain.agents import Tool

from ..python_tools.python_writer import PythonWriter
from .base_tool_manager import BaseToolManager


class PythonWriterToolManager(BaseToolManager):
    """
    PythonWriterToolManager
    A class for interacting with the PythonWriter API, which provides functionality to modify
    the code state of a given directory of Python files.
    """

    def __init__(
        self,
        python_writer: PythonWriter,
    ):
        """
        Initializes a PythonWriterToolManager object with the given inputs.

        Args:
        - python_writer (PythonWriter): A PythonWriter object representing the code writer to work with.
        - logger (Optional[PassThroughBuffer]): An optional PassThroughBuffer object to log output.

        Returns:
        - None
        """
        self.python_writer = python_writer

    def writer_update_module(self, input_str: str) -> str:
        print("Input Path:\n%s" % (input_str))
        module_path = input_str.split(",")[0]
        class_name = input_str.split(",")[1]
        print("class_name = ", class_name)
        code = ",".join(input_str.split(",")[2:]).strip()
        try:
            print("Writing to module_path - " + module_path)
            self.python_writer.update_module(
                source_code=code,
                extending_module=True,
                module_path=module_path,
                write_to_disk=True,
            )
            return "Success"
        except Exception as e:
            return "Failed to update the module with error - " + str(e)

    def build_tools(self) -> List[Tool]:
        """
        Builds a list of Tool object for interacting with PythonWriter.

        Args:
        - None

        Returns:
        - tools (List[Tool]): A list of Tool objects representing PythonWriter commands.
        """
        tools = [
            Tool(
                name="python-writer-update-module",
                func=lambda path_comma_code_str: self.writer_update_module(path_comma_code_str),
                description=f"Modifies the in-memory python code of a function, class, method, or module after receiving"
                f" an input python-path and code string. If the specified object or dependencies do not exist,"
                f" then they are created automatically. If the object already exists,"
                f" then it is modified the existing code."
                f" For example -"
                f' suppose you wish to a new function named "my_function" of "my_class" is defined in the file "my_file.py" that exists in "my_folder".'
                f" Then, the correct function call is "
                f'{{"tool": "python-writer-update-module",'
                f' "input": "my_folder.my_file,my_class,def my_function() -> None:\n   """My Function"""\n    print("hello world")"}}.'
                f" If new import statements are necessary, then append them to the top of the code string. Do not forget to wrap your input in double quotes.",
                return_direct=True,
            ),
        ]
        return tools
