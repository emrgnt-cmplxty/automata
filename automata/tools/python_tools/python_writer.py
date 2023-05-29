"""
This class provides methods for creating AST nodes from source code strings, and updating existing module objects with new code.
It also allows for extending and reducing module functionality by adding, updating or removing classes, methods, and functions.

Classes:
    PythonWriter: A utility class for manipulating and writing out Python AST nodes.

Example usage:

    ast_wrapper = PythonWriter()

    # Extend a module with new or updated code
    code_to_extend = '''
        def new_function():
            print("New function added")

        class ExistingClass:
            def new_method(self):
                print("New method added")
    '''
    extended_module = ast_wrapper.extend_module(code_to_extend, module_obj=existing_module)

    # Reduce a module by removing code
    code_to_reduce = '''
        def function_to_remove():
            pass

        class ClassToRemove:
            pass
    '''
    reduced_module = ast_wrapper.update_module(code_to_reduce, module_obj=existing_module)

    TODO - Add explicit check of module contents after extension and reduction of module.
"""
import logging
import re
import subprocess
from typing import Optional, Union, cast

from redbaron import ClassNode, Node, NodeList, RedBaron

from automata.core.code_indexing.python_code_retriever import PythonCodeRetriever
from automata.core.code_indexing.syntax_tree_navigation import (
    find_all_function_and_class_syntax_tree_nodes,
    find_import_syntax_tree_node_by_name,
    find_import_syntax_tree_nodes,
    find_syntax_tree_node,
)

logger = logging.getLogger(__name__)


class PythonWriter:
    """
    A utility class for working with Python AST nodes.

    Public Methods:

        update_module(
            source_code: str,
            module_obj (Optional[Module], keyword),
            module_path (Optional[str], keyword)
        ) -> None:
            Perform an in-place extention or reduction of a module object according to the received code.

        write_module(self) -> None:
            Write the module object to a file.

        Exceptions:
            ModuleNotFound: Raised when a module cannot be found.
            InvalidArguments: Raised when invalid arguments are passed to a method.
    """

    class ModuleNotFound(Exception):
        pass

    class ClassNotFound(Exception):
        pass

    class InvalidArguments(Exception):
        pass

    def __init__(self, python_retriever: PythonCodeRetriever):
        """
        Initialize the PythonWriter with a PythonCodeRetriever instance.
        """
        self.code_retriever = python_retriever

    def update_module(self, source_code: str, do_extend: bool = True, **kwargs) -> None:
        """
        Perform an in-place extention or reduction of a module object according to the received code.

        Args:
            source_code (str): The source_code containing the updates or deletions.
            do_extend (bool): True for adding/updating, False for reducing/deleting.
            module_obj (Optional[Module], keyword): The module object to be updated.
            module_path (Optional[str], keyword): The path of the module to be updated.
            class_name (Optional[str], keyword): The name of the class where the update should be applied, will default to module.
            write_to_disk (Optional[bool], keyword): Writes the changed module to disk.

        Raises:
            InvalidArguments: If both module_obj and module_dotpath are provided or none of them.

        Returns:
            Module: The updated module object.
        """
        module_obj = kwargs.get("module_obj")
        module_dotpath = kwargs.get("module_dotpath")
        class_name = kwargs.get("class_name") or ""
        write_to_disk = kwargs.get("write_to_disk") or False

        logger.info(
            "\n---Updating module---\nPath:\n%s\nClass Name:\n%s\nSource Code:\n%s\nWriting to disk:\n%s\n"
            % (module_dotpath, class_name, source_code, write_to_disk)
        )

        self._validate_args(module_obj, module_dotpath, write_to_disk)
        source_code = PythonWriter._clean_input_code(source_code)

        if module_dotpath:
            module_dotpath = cast(str, module_dotpath)

        # christ on a bike
        is_new_module = (
            not module_obj
            and module_dotpath
            and module_dotpath not in self.code_retriever.module_tree_map
        )

        is_existing_module = (
            module_obj
            and self.code_retriever.module_tree_map.get_existing_module_dotpath(module_obj)
            or module_dotpath in self.code_retriever.module_tree_map
        )

        if is_new_module:
            self._create_module_from_source_code(module_dotpath, source_code)
        elif is_existing_module:
            if module_obj:
                module_dotpath = self.code_retriever.module_tree_map.get_existing_module_dotpath(
                    module_obj
                )
            module_obj = self.code_retriever.module_tree_map.get_module(module_dotpath)
            PythonWriter._update_module(
                source_code,
                module_dotpath,
                module_obj,
                do_extend,
                class_name,
            )
        else:
            raise PythonWriter.InvalidArguments(
                f"Module is neither new nor existing, somehow: {module_dotpath}"
            )

        if write_to_disk:
            self.write_module(module_dotpath)

    def write_module(self, module_dotpath: str) -> None:
        """
        Write the modified module to a file at the specified output path.

        Args:
            module_dotpath (str): The file path where the modified module should be written.
        """
        if module_dotpath not in self.code_retriever.module_tree_map:
            raise PythonWriter.ModuleNotFound(
                f"Module not found in module dictionary: {module_dotpath}"
            )
        source_code = self.code_retriever.get_source_code(module_dotpath)
        module_fpath = self.code_retriever.module_tree_map.get_existing_module_fpath_by_dotpath(
            module_dotpath
        )
        with open(module_fpath, "w") as output_file:
            output_file.write(source_code)
        subprocess.run(["black", module_fpath])
        subprocess.run(["isort", module_fpath])

    def _create_module_from_source_code(self, module_dotpath: str, source_code: str) -> RedBaron:
        """
        Create a Python module from the given source code string.

        Args:
            module_dotpath (str): The path where the new module will be created.
        """
        parsed = RedBaron(source_code)
        self.code_retriever.module_tree_map.put_module(module_dotpath, parsed)
        return parsed

    @staticmethod
    def _validate_args(
        module_obj: Optional[RedBaron], module_dotpath: Optional[str], write_to_disk: bool
    ) -> None:
        """Validate the arguments passed to the update_module method."""
        if not (module_obj or module_dotpath) or (module_obj and module_dotpath):
            raise PythonWriter.InvalidArguments(
                "Provide either 'module_obj' or 'module_path', not both or none."
            )
        if not module_dotpath and write_to_disk:
            raise PythonWriter.InvalidArguments(
                "Provide 'module_path' to write the module to disk."
            )

    @staticmethod
    def _update_module(
        source_code: str,
        module_dotpath: str,
        existing_module_obj: RedBaron,
        do_extend: bool,
        class_name: str = "",
    ) -> None:
        """
        Update a module object according to the received code.

        Args:
            source_code (str): The code containing the updates.
            module_dotpath (str): The relative path to the module.
            existing_module_obj Module: The module object to be updated.
            do_extend (bool): If True, add or update the code; if False, remove the code.
        """

        new_fst = RedBaron(source_code)
        new_import_nodes = find_import_syntax_tree_nodes(new_fst)
        PythonWriter._manage_imports(existing_module_obj, new_import_nodes, do_extend)

        new_class_or_function_nodes = find_all_function_and_class_syntax_tree_nodes(new_fst)
        if class_name:  # splice the class
            existing_class = find_syntax_tree_node(existing_module_obj, class_name)
            if isinstance(existing_class, ClassNode):
                PythonWriter._update_node_with_children(
                    new_class_or_function_nodes, existing_class, do_extend
                )

            elif not do_extend:
                raise PythonWriter.ClassNotFound(
                    f"Class {class_name} not found in module {module_dotpath}"
                )
        PythonWriter._update_node_with_children(
            new_class_or_function_nodes, existing_module_obj, do_extend
        )

    @staticmethod
    def _update_node_with_children(
        class_or_function_nodes: NodeList,
        node_to_update: Union[ClassNode, RedBaron],
        do_extend: bool,
    ) -> None:
        """Update a class object according to the received code."""
        for new_node in class_or_function_nodes:
            child_node_name = new_node.name
            existing_node = find_syntax_tree_node(node_to_update, child_node_name)
            if do_extend:
                if existing_node:
                    existing_node.replace(new_node)
                else:
                    node_to_update.append(new_node)
            elif existing_node:
                PythonWriter.delete_node(existing_node)

    @staticmethod
    def delete_node(node: Node) -> None:
        """Delete a node from the FST."""
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
    def _manage_imports(
        module_obj: RedBaron, new_import_statements: NodeList, do_extend: bool
    ) -> None:
        """Manage the imports in the module."""
        for new_import_statement in new_import_statements:
            existing_import_statement = find_import_syntax_tree_node_by_name(
                module_obj, new_import_statement.name
            )
            if do_extend:
                if existing_import_statement:
                    existing_import_statement.replace(new_import_statement)
                else:
                    module_obj.append(new_import_statement)
            else:
                if existing_import_statement:
                    PythonWriter.delete_node(existing_import_statement)
