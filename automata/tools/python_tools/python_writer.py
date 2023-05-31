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

from redbaron import ClassNode, DefNode, Node, NodeList, RedBaron

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

    class ClassOrFunctionNotFound(Exception):
        pass

    class InvalidArguments(Exception):
        pass

    def __init__(self, python_retriever: PythonCodeRetriever):
        """
        Initialize the PythonWriter with a PythonCodeRetriever instance.
        """
        self.code_retriever = python_retriever

    def create_new_module(
        self, module_dotpath: str, source_code: str, do_write: bool = False
    ) -> None:
        """
        Create a new module object from source code.

        Args:
            source_code (str): The source code of the module.
            module_dotpath (str): The path of the module.

        Returns:
            RedBaron: The module object.
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
        Update code or insert new code into an existing module.

        Args:
            source_code (str): The source code of the part of the module that needs to be updated or insert.
            module_dotpath (str): The path of the module.
            disambiguator (Optional[str]): The name of the class or function scope where the update should be applied, will default to module.
            do_write (bool): Write the module to disk after updating.

        Returns:
            RedBaron: The module object.
        """
        module_obj = self.code_retriever.module_tree_map.get_module(module_dotpath)
        if not module_obj:
            raise PythonWriter.ModuleNotFound(
                f"Module not found in module dictionary: {module_dotpath}"
            )
        PythonWriter._update_existing_module(
            source_code,
            module_dotpath,
            module_obj,
            disambiguator=disambiguator,
        )
        if do_write:
            self._write_module_to_disk(module_dotpath)

    def delete_from_existing__module(
        self, module_dotpath: str, object_dotpath: str, do_write: bool = False
    ):
        """
        Reduce an existing module by removing a class or function.

        Args:
            module_dotpath (str): The path of the module.
            object_dotpath (str): The name of the class or function to remove, including the name of the scope it is in, like ClassName.function_name
            do_write (bool): Write the module to disk after updating.

        Returns:
            RedBaron: The module object.
        """
        module_obj = self.code_retriever.module_tree_map.get_module(module_dotpath)
        if not module_obj:
            raise PythonWriter.ModuleNotFound(
                f"Module not found in module dictionary: {module_dotpath}"
            )
        node = find_syntax_tree_node(module_obj, object_dotpath)
        if node:
            PythonWriter._delete_node(node)
            if do_write:
                self._write_module_to_disk(module_dotpath)

    def _write_module_to_disk(self, module_dotpath: str) -> None:
        """
        Write the modified module to a file at the specified output path.

        Args:
            module_dotpath (str)
        """
        if module_dotpath not in self.code_retriever.module_tree_map:
            raise PythonWriter.ModuleNotFound(
                f"Module not found in module dictionary: {module_dotpath}"
            )
        source_code = self.code_retriever.get_source_code(module_dotpath)
        module_fpath = self.code_retriever.module_tree_map.get_existing_module_fpath_by_dotpath(
            module_dotpath
        )

        if not module_fpath:
            raise PythonWriter.ModuleNotFound(
                f"Module fpath found in module map for dotpath: {module_dotpath}"
            )
        module_fpath = cast(str, module_fpath)
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
    def _update_existing_module(
        source_code: str,
        module_dotpath: str,
        existing_module_obj: RedBaron,
        disambiguator: Optional[str],
    ) -> None:
        """
        Update a module object according to the received code.

        Args:
            source_code (str): The code containing the updates.
            module_dotpath (str): The relative path to the module.
            existing_module_obj Module: The module object to be updated.
            disambiguator (str): The name of the class or function scope to be updated, useful for nested definitions.
        """

        new_fst = RedBaron(source_code)
        new_import_nodes = find_import_syntax_tree_nodes(new_fst)
        PythonWriter._update_imports(existing_module_obj, new_import_nodes)

        new_class_or_function_nodes = find_all_function_and_class_syntax_tree_nodes(new_fst)
        if disambiguator:  # splice the class
            disambiguator_node = find_syntax_tree_node(existing_module_obj, disambiguator)
            if isinstance(disambiguator_node, (ClassNode, DefNode)):
                PythonWriter._update_node_with_children(
                    new_class_or_function_nodes,
                    disambiguator_node,
                )
            else:
                raise PythonWriter.ClassOrFunctionNotFound(
                    f"Node {disambiguator} not found in module {module_dotpath}"
                )
        PythonWriter._update_node_with_children(new_class_or_function_nodes, existing_module_obj)

    @staticmethod
    def _update_node_with_children(
        class_or_function_nodes: NodeList,
        node_to_update: Union[ClassNode, RedBaron],
    ) -> None:
        """Update a class object according to the received code."""
        for new_node in class_or_function_nodes:
            child_node_name = new_node.name
            existing_node = find_syntax_tree_node(node_to_update, child_node_name)
            if existing_node:
                existing_node.replace(new_node)
            else:
                node_to_update.append(new_node)

    @staticmethod
    def _delete_node(node: Node) -> None:
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
    def _update_imports(module_obj: RedBaron, new_import_statements: NodeList) -> None:
        """Manage the imports in the module."""
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
