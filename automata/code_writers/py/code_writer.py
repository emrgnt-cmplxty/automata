# import astor
import ast
import logging
import os
import re
import subprocess
from typing import Dict, List, Optional, Union, cast

import numpy as np

from automata.code_parsers.directory import DirectoryManager
from automata.code_parsers.py.reader import PyReader
from automata.core import find_imports, find_syntax_tree_node
from automata.singletons.py_module_loader import py_module_loader
from automata.symbol.base import Symbol
from automata.symbol_embedding.base import SymbolDocEmbedding

# import pypandoc

# from redbaron import ClassNode, DefNode, Node, NodeList, RedBaron -> Needs removal


logger = logging.getLogger(__name__)


class PyCodeWriter:
    """A utility class for writing Python code along AST nodes"""

    class ModuleNotFound(Exception):
        """Raised when a module is not found in the module dictionary"""

        pass

    class ClassOrFunctionNotFound(Exception):
        """Raised when a class or function is not found in the module"""

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
        self, module_dotpath: str, source_code: str, do_write: bool = False
    ) -> None:
        """
        Create a new module object from source code

        Args:
            source_code (str): The source code of the module
            module_dotpath (str): The path of the module

        Returns:
            RedBaron: The created module object
        """
        self._create_module_from_source_code(module_dotpath, source_code)
        if do_write:
            self._write_module_to_disk(module_dotpath)

    def update_existing_module(
        self,
        module_dotpath: str,
        source_code: str,
        disambiguator: Optional[str] = "",
        do_write: bool = False,
    ) -> None:
        """
        Update code or insert new code into an existing module

        Args:
            source_code (str): The source code of the part of the module that needs to be
            updated or insert module_dotpath (str): The path of the module
            disambiguator (Optional[str]): The name of the class or function scope where
                the update should be applied, will default to module
            do_write (bool): Write the module to disk after updating

        Returns:
            RedBaron: The updated module object

        Raises:
            ModuleNotFound: If the module is not found in the module dictionary
        """
        module_obj = py_module_loader.fetch_ast_module(module_dotpath)
        if not module_obj:
            raise PyCodeWriter.ModuleNotFound(
                f"Module not found in module dictionary: {module_dotpath}"
            )
        PyCodeWriter._update_existing_module(
            source_code,
            module_dotpath,
            module_obj,
        )
        if do_write:
            self._write_module_to_disk(module_dotpath)

    def delete_from_existing__module(
        self, module_dotpath: str, object_dotpath: str, do_write: bool = False
    ) -> None:
        """
        Reduce an existing module by removing a class or function

        Args:
            module_dotpath (str): The path of the module
            object_dotpath (str): The name of the class or function to remove, including
                the name of the scope it is in, like ClassName.function_name
            do_write (bool): Write the module to disk after updating

        Returns:
            RedBaron: The module object

        Raises:
            ModuleNotFound: If the module is not found in the module dictionary
        """
        module_obj = py_module_loader.fetch_ast_module(module_dotpath)
        if not module_obj:
            raise PyCodeWriter.ModuleNotFound(
                f"Module not found in module dictionary: {module_dotpath}"
            )
        # node = find_syntax_tree_node(module_obj, object_dotpath)
        # if node:
        #     PyCodeWriter._delete_node(node)
        #     if do_write:
        #         self._write_module_to_disk(module_dotpath)

    def _write_module_to_disk(self, module_dotpath: str) -> None:
        """
        Write the modified module to a file at the specified output path

        Args:
            module_dotpath (str)

        Raises:
            ModuleNotFound: If the module is not found in the module dictionary
        """
        if module_dotpath not in py_module_loader:
            raise PyCodeWriter.ModuleNotFound(
                f"Module not found in module dictionary: {module_dotpath}"
            )

        module_ast = py_module_loader.fetch_ast_module(module_dotpath)
        if module_ast:
            source_code = ast.unparse(module_ast)

            module_fpath = (
                py_module_loader.fetch_existing_module_fpath_by_dotpath(
                    module_dotpath
                )
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

    def _create_module_from_source_code(
        self, module_dotpath: str, source_code: str
    ) -> ast.Module:
        """
        Create a Python module from the given source code string

        Args:
            module_dotpath (str): The path where the new module will be created

        Returns:
            ast.Module: The created module object
        """
        parsed = ast.parse(source_code)
        py_module_loader.put_module(module_dotpath, parsed)
        return parsed

    @staticmethod
    def _update_existing_module(
        source_code: str,
        module_dotpath: str,
        existing_module_obj: ast.Module,
    ) -> None:
        """
        Update a module object according to the received code

        Args:
            source_code (str): The code containing the updates
            module_dotpath (str): The relative path to the module
            existing_module_obj Module: The module object to be updated
            disambiguator (str): The name of the class or function scope to
                be updated, useful for nested definitions

        Raises:
            ClassOrFunctionNotFound: If the disambiguator is not found
        """

        new_module = ast.parse(source_code)
        # We first update the imports
        existing_import_nodes = [
            node
            for node in existing_module_obj.body
            if isinstance(node, (ast.Import, ast.ImportFrom))
        ]
        new_import_nodes = [
            node
            for node in new_module.body
            if isinstance(node, (ast.Import, ast.ImportFrom))
        ]

        for new_import_node in new_import_nodes:
            for existing_import_node in existing_import_nodes:
                # If the import already exists, we replace it
                if (
                    existing_import_node.names[0].name
                    == new_import_node.names[0].name
                ):
                    existing_import_node = new_import_node
                    break
            else:
                # If the import does not exist, we append it
                existing_module_obj.body.append(new_import_node)

        # Next, we update the class or function nodes
        existing_class_func_nodes = [
            node
            for node in existing_module_obj.body
            if isinstance(node, (ast.ClassDef, ast.FunctionDef))
        ]
        new_class_func_nodes = [
            node
            for node in new_module.body
            if isinstance(node, (ast.ClassDef, ast.FunctionDef))
        ]

        for new_node in new_class_func_nodes:
            for existing_node in existing_class_func_nodes:
                # If a node with the same name already exists, we replace it
                if existing_node.name == new_node.name:
                    existing_node = new_node
                    break
            else:
                # If the node does not exist, we append it
                existing_module_obj.body.append(new_node)

        # Finally, we update the module in the module loader
        py_module_loader.put_module(module_dotpath, existing_module_obj)

    @staticmethod
    def _clean_input_code(source_code: str) -> str:
        """
        Take the input source code and remove formatting issues that will cause the FST to fail.

        Args:
            source_code (str): The source code to clean.

        Returns:
            str: The cleaned source code.
        """

        def replace_newline_chars(input_str: str) -> str:
            dummy_replacement_a = "ZZ_^^_ZZ"
            dummy_replacement_b = "QQ_^^_QQ"

            def replace(match):
                text = match.group(0)
                if text[0] == '"' and text[-1] == '"':
                    return text
                return text.replace("\\n", "\n")

            pattern = "(?x)\n                '.*?'\n                |\n                \".*?\"\n                |\n                [^'\"]+\n            "
            output_str = (
                "".join(
                    (
                        replace(match)
                        for match in re.finditer(
                            pattern,
                            input_str.replace(
                                '"""', dummy_replacement_a
                            ).replace("'''", dummy_replacement_b),
                        )
                    )
                )
                .replace(dummy_replacement_a, '"""')
                .replace(dummy_replacement_b, "'''")
            )
            return output_str

        source_code = replace_newline_chars(source_code)
        source_code = re.sub('\\\\\\"', '"', source_code)
        source_code = source_code.strip()
        return source_code
