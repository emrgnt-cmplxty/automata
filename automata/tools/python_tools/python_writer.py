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
    extended_module = ast_wrapper.extend_module(code_to_extend, extending_module=True, module_obj=existing_module)

    # Reduce a module by removing code
    code_to_reduce = '''
        def function_to_remove():
            pass

        class ClassToRemove:
            pass
    '''
    reduced_module = ast_wrapper.update_module(code_to_reduce, extending_module=False, module_obj=existing_module)

    TODO - Add explicit check of module contents after extension and reduction of module.
"""
import os
import re
import subprocess
from typing import Optional, Union, cast

from redbaron import ClassNode, Node, NodeList, RedBaron

from automata.tools.python_tools.python_indexer import PythonIndexer


class PythonWriter:
    """
    A utility class for working with Python AST nodes.

    Public Methods:

        update_module(
            source_code: str,
            extending_module: bool,
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

    def __init__(self, python_indexer: PythonIndexer):
        """
        Initialize the PythonWriter with a PythonIndexer instance.
        """
        self.indexer = python_indexer

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
            InvalidArguments: If both module_obj and module_path are provided or none of them.

        Returns:
            Module: The updated module object.
        """
        module_obj = kwargs.get("module_obj")
        module_path = kwargs.get("module_path")
        class_name = kwargs.get("class_name") or ""

        write_to_disk = kwargs.get("write_to_disk") or False
        self._validate_args(module_obj, module_path, write_to_disk)
        source_code = PythonWriter._clean_input_code(source_code)

        if module_path:
            module_path = cast(str, module_path)

        # christ on a bike
        is_new_module = (
            not module_obj and module_path and module_path not in self.indexer.module_dict
        )

        is_existing_module = (
            module_obj
            and self.indexer.get_module_path(module_obj) != PythonIndexer.NO_RESULT_FOUND_STR
            or module_path in self.indexer.module_dict
        )

        if is_new_module:
            self._create_module_from_source_code(module_path, source_code)
        elif is_existing_module:
            if module_obj:
                module_path = self.indexer.get_module_path(module_obj)
            module_obj = self.indexer.module_dict[module_path]

            PythonWriter._update_module(
                source_code,
                module_path,
                module_obj,
                do_extend,
                class_name,
            )
        else:
            raise PythonWriter.InvalidArguments(
                f"Module is neither new nor existing, somehow: {module_path}"
            )

        if write_to_disk:
            self.write_module(module_path)

    def write_module(self, module_path: str) -> None:
        """
        Write the modified module to a file at the specified output path.

        Args:
            module_path (str): The file path where the modified module should be written.
        """
        if module_path not in self.indexer.module_dict:
            raise PythonWriter.ModuleNotFound(
                f"Module not found in module dictionary: {module_path}"
            )
        source_code = self.indexer.retrieve_code(module_path)
        module_os_rel_path = module_path.replace(self.indexer.PATH_SEP, os.path.sep)
        module_os_abs_path = os.path.join(self.indexer.abs_path, module_os_rel_path)
        os.makedirs(os.path.dirname(module_os_abs_path), exist_ok=True)
        file_path = f"{module_os_abs_path}.py"
        with open(file_path, "w") as output_file:
            output_file.write(source_code)
        subprocess.run(["black", file_path])
        subprocess.run(["isort", file_path])

    def _create_module_from_source_code(self, module_path: str, source_code: str) -> RedBaron:
        """
        Create a Python module from the given source code string.

        Args:
            module_path (str): The path where the new module will be created.
        """
        parsed = RedBaron(source_code)
        self.indexer.module_dict[module_path] = parsed  # TODO refactor to pure function
        return parsed

    @staticmethod
    def _validate_args(
        module_obj: Optional[RedBaron], module_path: Optional[str], write_to_disk: bool
    ) -> None:
        """Validate the arguments passed to the update_module method."""
        if not (module_obj or module_path) or (module_obj and module_path):
            raise PythonWriter.InvalidArguments(
                "Provide either 'module_obj' or 'module_path', not both or none."
            )
        if not module_path and write_to_disk:
            raise PythonWriter.InvalidArguments(
                "Provide 'module_path' to write the module to disk."
            )

    @staticmethod
    def _update_module(
        source_code: str,
        module_path: str,
        existing_module_obj: RedBaron,
        do_extend: bool,
        class_name: str = "",
    ) -> None:
        """
        Update a module object according to the received code.

        Args:
            source_code (str): The code containing the updates.
            module_path (str): The relative path to the module.
            existing_module_obj Module: The module object to be updated.
            do_extend (bool): If True, add or update the code; if False, remove the code.
        """

        new_fst = RedBaron(source_code)
        new_import_nodes = PythonIndexer.find_imports(new_fst)

        PythonWriter._manage_imports(existing_module_obj, new_import_nodes, do_extend)

        new_class_or_function_nodes = PythonIndexer.find_all_functions_and_classes(new_fst)
        # handle imports here later
        if class_name:  # splice the class
            existing_class = PythonIndexer.find_module_class_function_or_method(
                existing_module_obj, class_name
            )
            if not existing_class:
                raise PythonWriter.ClassNotFound(
                    f"Class {class_name} not found in module {module_path}"
                )
            if not isinstance(existing_class, ClassNode):
                raise PythonWriter.ClassNotFound(
                    f"Object {class_name} in module {module_path} is not a class."
                )
            PythonWriter._update_node_with_children(
                new_class_or_function_nodes, existing_class, do_extend
            )
        else:
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
            existing_node = PythonIndexer.find_module_class_function_or_method(
                node_to_update, child_node_name
            )
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
                            input_str.replace('"""', "ZZ_^^_ZZ").replace("'''", "QQ_^^_QQ"),
                        )
                    )
                )
                .replace("ZZ_^^_ZZ", '"""')
                .replace("QQ_^^_QQ", "'''")
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
            existing_import_statement = PythonIndexer.find_import_by_name(
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
