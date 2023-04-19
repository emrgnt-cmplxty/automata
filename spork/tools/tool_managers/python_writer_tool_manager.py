from typing import List, Optional

from langchain.agents import Tool

from ..python_tools.python_writer import PythonWriter
from ..utils import PassThroughBuffer
from .base_tool_manager import BaseToolManager


class PythonWriterToolManager(BaseToolManager):
    """
    PythonWriterToolManager
    A class for interacting with the PythonWriter API, which provides functionality to modify
    the code state of a given directory of Python files.
    """

    def __init__(self, python_writer: PythonWriter, logger: Optional[PassThroughBuffer] = None):
        """
        Initializes a PythonWriterToolManager object with the given inputs.

        Args:
        - python_writer (PythonWriter): A PythonWriter object representing the code writer to work with.
        - logger (Optional[PassThroughBuffer]): An optional PassThroughBuffer object to log output.

        Returns:
        - None
        """
        self.python_writer = python_writer
        self.logger = logger

    def python_writer_wrapper(self, input_str: str) -> str:
        path = input_str.split(",")[0]
        code = ",".join(input_str.split(",")[1:]).strip()
        return self.python_writer.modify_code_state(
            *(
                path,
                code,
            )
        )

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
                name="python-writer-modify-code-state",
                func=lambda python_path_comma_code_str: self.python_writer_wrapper(
                    python_path_comma_code_str
                ),
                description=f"Modifies the in-memory python code of a function, class, method, or module after receiving"
                f" an input python-path and code string. If the specified object or dependencies do not exist,"
                f" then they are created automatically. If the object already exists,"
                f" then it is modified the existing code."
                f" For example -"
                f' suppose you wish to a new function named "my_function" of "my_class" is defined in the file "my_file.py" that lives in "my_folder".'
                f" Then, the correct function call is "
                f'{{"tool": "python-writer-modify-code-state",'
                f' "input": "my_folder.my_file,def my_function() -> None:\n   """My Function"""\n    print("hello world")}}.'
                f" If new import statements are necessary, then append them to the top of the code string. Do not forget to wrap your input in double quotes.",
                return_direct=True,
            ),
            Tool(
                name="python-writer-write-to-disk",
                func=lambda _: self.python_writer.write_to_disk(),
                description=f"Writes all the latest modifications in the code state to disk."
                " New files are created automatically where necessary.",
                return_direct=True,
            ),
        ]
        return tools
