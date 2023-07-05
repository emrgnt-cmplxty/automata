import logging
import os
import re
import subprocess
from typing import Dict, List, Optional, Union, cast

import numpy as np
import pypandoc
from redbaron import ClassNode, DefNode, Node, NodeList, RedBaron

from automata.core.code_handling.py.reader import PyReader
from automata.core.navigation.directory import DirectoryManager
from automata.core.navigation.py.navigation_utils import (
    find_all_function_and_class_syntax_tree_nodes,
    find_import_syntax_tree_node_by_name,
    find_import_syntax_tree_nodes,
    find_syntax_tree_node,
)
from automata.core.singletons.py_module_loader import py_module_loader
from automata.core.symbol.base import Symbol
from automata.core.symbol_embedding.base import SymbolDocEmbedding

logger = logging.getLogger(__name__)


class PyWriter:
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
        Initialize the PyWriter with a PyReader instance

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
        module_obj = py_module_loader.fetch_module(module_dotpath)
        if not module_obj:
            raise PyWriter.ModuleNotFound(
                f"Module not found in module dictionary: {module_dotpath}"
            )
        PyWriter._update_existing_module(
            source_code,
            module_dotpath,
            module_obj,
            disambiguator=disambiguator,
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
        module_obj = py_module_loader.fetch_module(module_dotpath)
        if not module_obj:
            raise PyWriter.ModuleNotFound(
                f"Module not found in module dictionary: {module_dotpath}"
            )
        node = find_syntax_tree_node(module_obj, object_dotpath)
        if node:
            PyWriter._delete_node(node)
            if do_write:
                self._write_module_to_disk(module_dotpath)

    def _write_module_to_disk(self, module_dotpath: str) -> None:
        """
        Write the modified module to a file at the specified output path

        Args:
            module_dotpath (str)

        Raises:
            ModuleNotFound: If the module is not found in the module dictionary
        """
        if module_dotpath not in py_module_loader:
            raise PyWriter.ModuleNotFound(
                f"Module not found in module dictionary: {module_dotpath}"
            )

        source_code = self.py_reader.get_source_code(module_dotpath)
        module_fpath = py_module_loader.fetch_existing_module_fpath_by_dotpath(module_dotpath)

        if not module_fpath:
            raise PyWriter.ModuleNotFound(
                f"Module fpath found in module map for dotpath: {module_dotpath}"
            )
        module_fpath = cast(str, module_fpath)
        with open(module_fpath, "w") as output_file:
            output_file.write(source_code)
        subprocess.run(["black", module_fpath])
        subprocess.run(["isort", module_fpath])

    def _create_module_from_source_code(self, module_dotpath: str, source_code: str) -> RedBaron:
        """
        Create a Python module from the given source code string

        Args:
            module_dotpath (str): The path where the new module will be created

        Returns:
            RedBaron: The created module object
        """
        parsed = RedBaron(source_code)
        py_module_loader.put_module(module_dotpath, parsed)
        return parsed

    @staticmethod
    def _update_existing_module(
        source_code: str,
        module_dotpath: str,
        existing_module_obj: RedBaron,
        disambiguator: Optional[str],
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

        new_fst = RedBaron(source_code)
        new_import_nodes = find_import_syntax_tree_nodes(new_fst)
        PyWriter._update_imports(existing_module_obj, new_import_nodes)

        new_class_or_function_nodes = find_all_function_and_class_syntax_tree_nodes(new_fst)
        if disambiguator:  # splice the class
            disambiguator_node = find_syntax_tree_node(existing_module_obj, disambiguator)
            if isinstance(disambiguator_node, (ClassNode, DefNode)):
                PyWriter._update_node_with_children(
                    new_class_or_function_nodes,
                    disambiguator_node,
                )
            else:
                raise PyWriter.ClassOrFunctionNotFound(
                    f"Node {disambiguator} not found in module {module_dotpath}"
                )
        PyWriter._update_node_with_children(new_class_or_function_nodes, existing_module_obj)

    @staticmethod
    def _update_node_with_children(
        class_or_function_nodes: NodeList,
        node_to_update: Union[ClassNode, RedBaron],
    ) -> None:
        """
        Update a class object according to the received code

        Args:
            class_or_function_nodes (NodeList): The nodes to update
            node_to_update (Union[ClassNode, RedBaron]): The node to update
        """
        for new_node in class_or_function_nodes:
            child_node_name = new_node.name
            existing_node = find_syntax_tree_node(node_to_update, child_node_name)
            if existing_node:
                existing_node.replace(new_node)
            else:
                node_to_update.append(new_node)

    @staticmethod
    def _delete_node(node: Node) -> None:
        """
        Delete a node from the FST

        Args:
            node (Node): The node to delete
        """
        parent = node.parent
        parent_index = node.index_on_parent
        parent.pop(parent_index)

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
                            input_str.replace('"""', dummy_replacement_a).replace(
                                "'''", dummy_replacement_b
                            ),
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

    @staticmethod
    def _update_imports(module_obj: RedBaron, new_import_statements: NodeList) -> None:
        """
        Manage the imports in the module

        Args:
            module_obj (RedBaron): The module object
            new_import_statements (NodeList): The new import statements

        """
        first_import = module_obj.find(lambda identifier: identifier in ("import", "from_import"))

        for new_import_statement in new_import_statements:
            existing_import_statement = find_import_syntax_tree_node_by_name(
                module_obj, new_import_statement.name
            )
            if not existing_import_statement:
                if first_import:
                    first_import.insert_before(new_import_statement)  # we will run isort later
                else:
                    module_obj.insert(0, new_import_statement)


class PyDocWriter:
    """A class to write documentation for Python modules"""

    def __init__(self, base_path: str) -> None:
        """
        Args:
            base_path (str): The base path of the project
        """
        self.base_path = base_path
        self.directory_manager = DirectoryManager(base_path)

    def generate_module_summary(self, module_dir: str) -> None:
        """
        Function to generate a module-level summary. Here, we just assume that
        all the .rst files in a directory correspond to the same module.
        We read these files, use their content to generate a summary using
        a language model and write this summary to the module's index.rst file.

        Args:
            module_dir (str): The directory of the module
        """
        summary = ""
        for file in self.directory_manager.get_files_in_dir(module_dir):
            if file.endswith(".rst") and file != "index.rst":
                with open(os.path.join(module_dir, file), "r") as f:
                    content = f.read()
                    summary += content + "\n\n"

        summary = self.generate_summary(summary)

        with open(os.path.join(module_dir, "index.rst"), "a") as f:
            f.write("\n\n" + summary)

    def generate_rst_files(
        self, docs: Dict[Symbol, SymbolDocEmbedding], symbols: List[Symbol], docs_dir: str
    ) -> None:
        """
        Generate individual .rst files for each key (a key represents a module)
            and updates the file structure.

        Args:
            docs (Dict[Any, Any]): The documentation dictionary
            symbols (List[Any]): The symbols of the documentation dictionary
            docs_dir (str): The output directory for the docs
        """
        for symbol in np.array(symbols):
            symbol_name = symbol.descriptors[-1].name

            if symbol_name[0] == "_" or not PyDocWriter.check_camel_case(symbol_name):
                continue

            snaked_symbol_name = PyDocWriter.camel_to_snake(symbol_name)
            module_dir = "/".join(symbol.dotpath.split(".")[1:-2])

            new_module_dir = os.path.join(docs_dir, module_dir)
            self.directory_manager.ensure_directory_exists(new_module_dir)

            with open(os.path.join(new_module_dir, f"{snaked_symbol_name}.rst"), "w") as f:
                try:
                    doc_md_string = docs[symbol].input_object
                    rst_string = pypandoc.convert_text(doc_md_string, "rst", format="md")
                    f.write(rst_string)
                except Exception as e:
                    logger.error(f"Error converting {symbol_name} to rst: {e}")

    def generate_index_files(self, docs_dir: str) -> None:
        """
        Generate index files for each directory that
            contains .rst files or subdirectories.

        Args:
            docs_dir (str): The output directory for the docs
        """
        doc_directory_manager = DirectoryManager(docs_dir)
        for root, dirs, _ in os.walk(docs_dir, topdown=False):
            root_relative_to_base = os.path.relpath(root, start=docs_dir)
            files = doc_directory_manager.get_files_in_dir(root_relative_to_base)
            dirs = doc_directory_manager.get_subdirectories(root_relative_to_base)

            rst_files = [f for f in files if f.endswith(".rst")]
            root_dir_node = doc_directory_manager._get_node_for_path(
                doc_directory_manager.root, root_relative_to_base
            )

            index_path = os.path.join(root, "index.rst")
            if rst_files or dirs:
                if os.path.exists(index_path):
                    with open(index_path, "r") as index_file:
                        existing_content = index_file.read()
                else:
                    existing_content = ""

                # Identify start and end of the auto-generated content
                auto_start_marker = "\n..  AUTO-GENERATED CONTENT START\n..\n\n"
                auto_end_marker = "\n..  AUTO-GENERATED CONTENT END\n..\n\n"

                # Remove the auto-generated part if it already exists
                if auto_start_marker in existing_content and auto_end_marker in existing_content:
                    start_idx = existing_content.index(auto_start_marker)
                    end_idx = existing_content.index(auto_end_marker) + len(auto_end_marker)
                    existing_content = existing_content[:start_idx] + existing_content[end_idx:]

                # Add new auto-generated content
                auto_content = auto_start_marker
                auto_content += "    .. toctree::\n"
                auto_content += (
                    "       :maxdepth: 2\n\n"
                    if not root_dir_node or root_dir_node.is_root_dir()  # type: ignore
                    else "       :maxdepth: 1\n\n"
                )
                for file in sorted(rst_files):
                    if file != "index.rst":
                        auto_content += f"       {file[:-4]}\n"  # Remove .rst extension
                for sub_dir_ in sorted(dirs):
                    auto_content += f"       {sub_dir_}/index\n"
                auto_content += auto_end_marker

                # Write everything back to the file
                with open(index_path, "w") as index_file:
                    if existing_content.strip() == "":
                        index_file.write(PyDocWriter.get_payload(root) + auto_content)
                    else:
                        index_file.write(existing_content + auto_content)

                self.generate_module_summary(root)

    def write_documentation(
        self, docs: Dict[Symbol, SymbolDocEmbedding], symbols: List[Symbol], docs_dir: str
    ) -> None:
        """
        Generate the full documentation given the symbols and a directory.

        Args:
            docs (Dict[Any, Any]): The documentation dictionary
            symbols (List[Any]): The symbols of the documentation dictionary
            docs_dir (str): The relative directory
        """
        self.generate_rst_files(docs, symbols, docs_dir)
        self.generate_index_files(docs_dir)

    @staticmethod
    def get_payload(directory: str) -> str:
        """Returns a formatted string for the main body of the index.rst file."""
        return f"""{os.path.basename(directory)}
{"=" * len(os.path.basename(directory))}

**Automata** is a Python library for autonomous providers.

Check out the :doc:`usage` section for further information, including
how to :ref:`installation` the project.


"""

    @staticmethod
    def generate_summary(content: str) -> str:
        """This method should implement the logic to generate summary from the content."""
        # TODO: Implement summary generation function.
        return ""

    @staticmethod
    def camel_to_snake(name: str) -> str:
        """
        Converts a camel case string to snake case

        Args:
            name (str): The string to convert

        Returns:
            str: The converted string
        """

        name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
        name = re.sub("([a-z0-9])([A-Z])", r"\1_\2", name)
        return name.lower()

    @staticmethod
    def check_camel_case(text: str) -> bool:
        """
        Checks if a string is camel case

        Args:
            text (str): The string to check

        Returns:
            bool: True if the string is camel case, False otherwise
        """
        return text != text.lower() and text != text.upper() and "_" not in text
