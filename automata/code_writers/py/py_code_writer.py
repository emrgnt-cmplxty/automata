"""Module containing functions to build SymbolDocEmbedding objects."""
import ast
import logging
import subprocess
from typing import cast

import automata.core.utils  # pylint: disable=unused-import
from automata.code_parsers.py.py_reader import PyReader
from automata.singletons.py_module_loader import py_module_loader

logger = logging.getLogger(__name__)


class PyCodeWriter:
    """A utility class for writing Python code along AST nodes"""

    class ModuleNotFoundError(Exception):
        """Raised when a module is not found in the module dictionary"""

        pass

    class StatementNotFoundError(Exception):
        """Raised when a provided ast.Statement is not found in the module"""

        pass

    class InvalidArgumentsError(Exception):
        """Raised when invalid arguments are passed to a method"""

        pass

    def __init__(self, py_reader: PyReader) -> None:
        self.py_reader = py_reader

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PyCodeWriter):
            return False
        # Since there are no internal variables, just check if other is an
        # instance of PyReader
        return self.py_reader == other.py_reader and isinstance(
            other, PyCodeWriter
        )

    def create_new_module(
        self, module_dotpath: str, module: ast.Module, do_write: bool = False
    ) -> None:
        """
        Create a new module object from source code, with option to write to disk.

        Raises:
            PyCodeWriter.InvalidArgumentsError: If the module already exists in the module dictionary.
            PyCodeWriter.ModuleNotFoundError: If the module writeout fails.
        """
        if module_dotpath in py_module_loader:
            raise PyCodeWriter.InvalidArgumentsError(
                "Module already exists in module dictionary."
            )
        py_module_loader.put_module(module_dotpath, module)
        if do_write:
            self.write_module_to_disk(module_dotpath)

    def write_module_to_disk(self, module_dotpath: str) -> None:
        """Write the modified module to a file at the specified output path

        Raises:
            ModuleNotFoundError: If the module is not found in the module dictionary
        """
        if not (
            module_ast := py_module_loader.fetch_ast_module(module_dotpath)
        ):
            raise PyCodeWriter.ModuleNotFoundError(
                f"Module fpath found in module map for dotpath: {module_dotpath}"
            )
        source_code = ast.unparse(module_ast)

        module_fpath = py_module_loader.fetch_existing_module_fpath_by_dotpath(
            module_dotpath
        )

        if not module_fpath:
            raise PyCodeWriter.ModuleNotFoundError(
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
        nodes = {getattr(node, "name", None): node for node in module.body}

        for new_node in new_module.body:
            new_node_name = getattr(new_node, "name", None)

            # If the new node already exists in the module, remove the old node.
            if new_node_name in nodes:
                module.body.remove(nodes[new_node_name])

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
        nodes = {getattr(node, "name", None): node for node in module.body}

        for deletion_node in deletion_module.body:
            deletion_node_name = getattr(deletion_node, "name", None)

            # If the node to be deleted is not found in the module, raise an exception.
            if deletion_node_name not in nodes:
                raise PyCodeWriter.StatementNotFoundError(
                    f"Node with name '{deletion_node_name}' not found in module"
                )

            # Delete the node from the module body.
            module.body.remove(nodes[deletion_node_name])

    def delete_module(self, module_dotpath: str) -> None:
        """
        Create a new module object from source code, with option to write to disk.

        Raises:
            PyCodeWriter.InvalidArgumentsError: If the module already exists in the module dictionary.
            PyCodeWriter.ModuleNotFoundError: If the module writeout fails.
        """
        if module_dotpath not in py_module_loader:
            raise PyCodeWriter.InvalidArgumentsError(
                "Module does not exist in module dictionary."
            )
        py_module_loader.delete_module(module_dotpath)
