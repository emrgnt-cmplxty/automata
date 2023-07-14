import logging
import os
import re
from typing import TYPE_CHECKING, Dict, List

import numpy as np
import pypandoc

from automata.code_parsers import DirectoryManager

if TYPE_CHECKING:
    from automata.symbol import Symbol
    from automata.symbol_embedding import SymbolDocEmbedding

logger = logging.getLogger(__name__)


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
        self,
        docs: Dict["Symbol", "SymbolDocEmbedding"],
        symbols: List["Symbol"],
        docs_dir: str,
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
            module_dir = "/".join(symbol.full_dotpath.split(".")[1:-2])

            new_module_dir = os.path.join(docs_dir, module_dir)
            self.directory_manager.ensure_directory_exists(new_module_dir)

            with open(
                os.path.join(new_module_dir, f"{snaked_symbol_name}.rst"), "w"
            ) as f:
                try:
                    doc_md_string = docs[symbol].document
                    rst_string = pypandoc.convert_text(
                        doc_md_string, "rst", format="md"
                    )
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
                if (
                    auto_start_marker in existing_content
                    and auto_end_marker in existing_content
                ):
                    start_idx = existing_content.index(auto_start_marker)
                    end_idx = existing_content.index(auto_end_marker) + len(
                        auto_end_marker
                    )
                    existing_content = (
                        existing_content[:start_idx] + existing_content[end_idx:]
                    )

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
        self,
        docs: Dict["Symbol", "SymbolDocEmbedding"],
        symbols: List["Symbol"],
        docs_dir: str,
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
