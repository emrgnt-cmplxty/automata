import logging
from typing import List, Optional

from automata.core.base.tool import Tool
from automata.core.coding.py.writer import PyWriter

from .agent_tool import AgentTool

logger = logging.getLogger(__name__)


class PyWriterTool(AgentTool):
    """
    PyWriterTool
    A class for interacting with the PythonWriter API, which provides functionality to modify
    the code state of a given directory of Python files.
    """

    def __init__(
        self,
        py_writer: PyWriter,
        **kwargs,
    ) -> None:
        """
        Initializes a PyWriterTool object with the given inputs.

        Args:
        - writer (PythonWriter): A PythonWriter object representing the code writer to work with.

        Returns:
        - None
        """
        self.writer = py_writer
        self.model = kwargs.get("model", "gpt-4")
        self.verbose = kwargs.get("verbose", False)
        self.stream = kwargs.get("stream", True)
        self.temperature = kwargs.get("temperature", 0.7)
        self.do_write = kwargs.get("do_write", True)

    def build(self) -> List[Tool]:
        """
        Builds the tools associated with the python code writer.

        Returns:
            List[Tool]: The list of built tools.
        """
        return [
            Tool(
                name="py-writer-update-module",
                func=lambda module_object_code_tuple: self._update_existing_module(
                    *module_object_code_tuple
                ),
                description=f"Inserts or updates the python code of a function, class, method in an existing module"
                f" If a given object or its child object do not exist,"
                f" then they are created automatically. If the object already exists, then the existing code is modified."
                f" For example -"
                f' to implement a method "my_method" of "MyClass" in the module "my_file.py" which exists in "my_folder",'
                f" the correct function call follows:\n"
                f" - tool_query_1\n"
                f"   - tool_name\n"
                f"     - py-writer-update-module\n"
                f"   - tool_args\n"
                f"     - my_folder.my_file\n"
                f"     - MyClass\n"
                f'     - def my_method():\n   """My Method"""\n    print("hello world")\n'
                f"If new import statements are necessary, then introduce them at the top of the submitted input code.\n"
                f"Provide the full code as input, as this tool has no context outside of passed arguments.\n",
                return_direct=True,
            ),
            Tool(
                name="py-writer-create-new-module",
                func=lambda module_object_code_tuple: self._create_new_module(
                    *module_object_code_tuple
                ),
                description=f"Creates a new module at the given path with the given code. For example:"
                f" - tool_query_1\n"
                f"   - tool_name\n"
                f"     - py-writer-create-new-module\n"
                f"   - tool_args\n"
                f"     - my_folder.my_file\n"
                f'     - import math\ndef my_method():\n   """My Method"""\n    print(math.sqrt(4))\n',
                return_direct=True,
            ),
            Tool(
                name="py-writer-delete-from-existing-module",
                func=lambda module_object_code_tuple: self._delete_from_existing_module(
                    *module_object_code_tuple
                ),
                description=f"Deletes python objects and their code by name from existing module. For example:"
                f" - tool_query_1\n"
                f"   - tool_name\n"
                f"     - py-writer-delete-from-existing-module\n"
                f"   - tool_args\n"
                f"     - my_folder.my_file\n"
                f"     - MyClass.my_method\n",
                return_direct=True,
            ),
        ]

    def _update_existing_module(
        self,
        module_dotpath: str,
        disambiguator: Optional[str],
        code: str,
    ) -> str:
        """
        Updates an existing module with the given code.

        Args:
            module_dotpath (str): The dotpath of the module to update.
            disambiguator (Optional[str]): The disambiguator of the module to update.
            code (str): The code to write to the module.

        Returns:
            str: The result of the update.
        """
        try:
            self.writer.update_existing_module(module_dotpath, code, disambiguator, self.do_write)
            return "Success"
        except Exception as e:
            return f"Failed to update the module with error - {str(e)}"

    def _delete_from_existing_module(
        self,
        module_dotpath: str,
        object_dotpath: str,
    ) -> str:
        """
        Deletes an object from an existing module.

        Args:
            module_dotpath (str): The dotpath of the module to update.
            object_dotpath (str): The dotpath of the object to delete.

        Returns:
            str: The result of the deletion.
        """
        try:
            self.writer.delete_from_existing__module(module_dotpath, object_dotpath, self.do_write)
            return "Success"
        except Exception as e:
            return f"Failed to reduce the module with error - {str(e)}"

    def _create_new_module(self, module_dotpath, code) -> str:
        """
        Creates a new module with the given code.

        Args:
            module_dotpath (str): The dotpath of the module to update.
            code (str): The code to write to the module.

        Returns:
            str: The result of the creation.
        """

        try:
            self.writer.create_new_module(module_dotpath, code, self.do_write)
            return "Success"
        except Exception as e:
            return f"Failed to create the module with error - {str(e)}"
