import ast
import logging
import subprocess
from typing import cast

from automata.code_parsers.py.reader import PyReader
from automata.singletons.py_module_loader import py_module_loader

logger = logging.getLogger(__name__)


class PyCodeWriter:
    """A utility class for writing Python code along AST nodes"""

    class ModuleNotFound(Exception):
        """Raised when a module is not found in the module dictionary"""

        pass

    class StatementNotFound(Exception):
        """Raised when a provided ast.Statement is not found in the module"""

        pass

    class InvalidArguments(Exception):
        """Raised when invalid arguments are passed to a method"""

        pass

    def __init__(self, py_reader: PyReader) -> None:
        """
        Initialize the PyCodeWriter with a PyReader instance

        Args:
            py_reader (PyReader): The PyReader instance to use
        """
        self.py_reader = py_reader

    def create_new_module(
        self, module_dotpath: str, module: ast.Module, do_write: bool = False
    ) -> None:
        """
        Create a new module object from source code, with option to write to disk.

        Raises:
            PyCodeWriter.InvalidArguments: If the module already exists in the module dictionary.
            PyCodeWriter.ModuleNotFound: If the module writeout fails.
        """
        if module_dotpath in py_module_loader:
            raise PyCodeWriter.InvalidArguments(
                "Module already exists in module dictionary."
            )
        py_module_loader.put_module(module_dotpath, module)
        if do_write:
            self.write_module_to_disk(module_dotpath)

    def write_module_to_disk(self, module_dotpath: str) -> None:
        """Write the modified module to a file at the specified output path

        Raises:
            ModuleNotFound: If the module is not found in the module dictionary
        """
        if not (
            module_ast := py_module_loader.fetch_ast_module(module_dotpath)
        ):
            raise PyCodeWriter.ModuleNotFound(
                f"Module fpath found in module map for dotpath: {module_dotpath}"
            )
        source_code = ast.unparse(module_ast)

        module_fpath = py_module_loader.fetch_existing_module_fpath_by_dotpath(
            module_dotpath
        )

        if not module_fpath:
            raise PyCodeWriter.ModuleNotFound(
                f"Module fpath found in module map for dotpath: {module_dotpath}"
            )
        module_fpath = cast(str, module_fpath)

        self._write_to_disk_and_format(module_fpath, source_code)

    def _write_to_disk_and_format(self, module_fpath: str, source_code: str):
        """Write the source code to disk and format it using black and isort."""

        with open(module_fpath, "w") as output_file:
            output_file.write(source_code)
        subprocess.run(["black", module_fpath])
        subprocess.run(["isort", module_fpath])

    def upsert_to_module(
        self, module: ast.Module, new_module: ast.Module
    ) -> None:
        """Upserts the nodes from a new_module into an existing module."""

        # For quick lookup, create a dictionary with key as the node name and value as the node.
        module_dict = {
            getattr(node, "name", None): node for node in module.body
        }

        for new_node in new_module.body:
            new_node_name = getattr(new_node, "name", None)

            # If the new node already exists in the module, remove the old node.
            if new_node_name in module_dict:
                module.body.remove(module_dict[new_node_name])

            # Add the new node (either as an insert or an update)
            module.body.append(new_node)

    def delete_from_module(
        self, module: ast.Module, deletion_module: ast.Module
    ) -> None:
        """
        Takes the contents of deletion_module and deletes them from module.

        Raises:
            PyCodeWriter.NodeNotFound: If any deletion_module nodes are not found in module.
        """

        # For quick lookup, create a dictionary with key as the node name and value as the node.
        module_dict = {
            getattr(node, "name", None): node for node in module.body
        }

        for deletion_node in deletion_module.body:
            deletion_node_name = getattr(deletion_node, "name", None)

            # If the node to be deleted is not found in the module, raise an exception.
            if deletion_node_name not in module_dict:
                raise PyCodeWriter.StatementNotFound(
                    f"Node with name '{deletion_node_name}' not found in module"
                )

            # Delete the node from the module body.
            module.body.remove(module_dict[deletion_node_name])

    def delete_module(self, module_dotpath: str) -> None:
        """
        Create a new module object from source code, with option to write to disk.

        Raises:
            PyCodeWriter.InvalidArguments: If the module already exists in the module dictionary.
            PyCodeWriter.ModuleNotFound: If the module writeout fails.
        """
        if module_dotpath not in py_module_loader:
            raise PyCodeWriter.InvalidArguments(
                "Module does not exist in module dictionary."
            )
        py_module_loader.delete_module(module_dotpath)
