import logging
from typing import List, Optional

from automata.config.config_types import AgentConfigName
from automata.core.base.tool import Tool
from automata.core.coding.py_coding.writer import PyCodeWriter

from .base_tool_manager import BaseToolManager

logger = logging.getLogger(__name__)


class PyCodeWriterToolManager(BaseToolManager):
    """
    PyCodeWriterToolManager
    A class for interacting with the PythonWriter API, which provides functionality to modify
    the code state of a given directory of Python files.
    """

    def __init__(
        self,
        **kwargs,
    ):
        """
        Initializes a PyCodeWriterToolManager object with the given inputs.

        Args:
        - writer (PythonWriter): A PythonWriter object representing the code writer to work with.

        Returns:
        - None
        """
        self.writer: PyCodeWriter = kwargs.get("python_writer")
        # TODO: unused
        self.automata_version = (
            kwargs.get("automata_version") or AgentConfigName.AUTOMATA_WRITER_PROD
        )
        self.model = kwargs.get("model", "gpt-4")
        self.verbose = kwargs.get("verbose", False)
        self.stream = kwargs.get("stream", True)
        self.temperature = kwargs.get("temperature", 0.7)
        self.do_write = kwargs.get("do_write", True)

    def build_tools(self) -> List[Tool]:
        """Builds a list of Tool object for interacting with PythonWriter."""
        tools = [
            Tool(
                name="python-writer-update-module",
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
                f"     - python-writer-update-module\n"
                f"   - tool_args\n"
                f"     - my_folder.my_file\n"
                f"     - MyClass\n"
                f'     - def my_method() -> None:\n   """My Method"""\n    print("hello world")\n'
                f"If new import statements are necessary, then introduce them at the top of the submitted input code.\n"
                f"Provide the full code as input, as this tool has no context outside of passed arguments.\n",
                return_direct=True,
            ),
            Tool(
                name="python-writer-create-new-module",
                func=lambda module_object_code_tuple: self._create_new_module(
                    *module_object_code_tuple
                ),
                description=f"Creates a new module at the given path with the given code. For example:"
                f" - tool_query_1\n"
                f"   - tool_name\n"
                f"     - python-writer-create-new-module\n"
                f"   - tool_args\n"
                f"     - my_folder.my_file\n"
                f'     - import math\ndef my_method() -> None:\n   """My Method"""\n    print(math.sqrt(4))\n',
                return_direct=True,
            ),
            Tool(
                name="python-writer-delete-from-existing-module",
                func=lambda module_object_code_tuple: self._delete_from_existing_module(
                    *module_object_code_tuple
                ),
                description=f"Deletes python objects and their code by name from existing module. For example:"
                f" - tool_query_1\n"
                f"   - tool_name\n"
                f"     - python-writer-delete-from-existing-module\n"
                f"   - tool_args\n"
                f"     - my_folder.my_file\n"
                f"     - MyClass.my_method\n",
                return_direct=True,
            ),
        ]
        return tools

    def _update_existing_module(
        self,
        module_dotpath: str,
        disambiguator: Optional[str],
        code: str,
    ) -> str:
        """Writes the given code to the given module path and class name."""
        try:
            print("Attempting to write update to existing module_path = ", module_dotpath)
            self.writer.update_existing_module(module_dotpath, code, disambiguator, self.do_write)
            return "Success"
        except Exception as e:
            return "Failed to update the module with error - " + str(e)

    def _delete_from_existing_module(
        self,
        module_dotpath: str,
        object_dotpath: str,
    ) -> str:
        """Writes the given code to the given module path and class name."""
        try:
            print("Attempting to reduce existing module_path = ", module_dotpath)
            self.writer.delete_from_existing__module(module_dotpath, object_dotpath, self.do_write)
            return "Success"
        except Exception as e:
            return "Failed to reduce the module with error - " + str(e)

    def _create_new_module(self, module_dotpath, code):
        """Writes the given code to the given module path and class name."""
        try:
            print("Attempting to write new module_path = ", module_dotpath)
            self.writer.create_new_module(module_dotpath, code, self.do_write)
            return "Success"
        except Exception as e:
            return "Failed to create the module with error - " + str(e)
