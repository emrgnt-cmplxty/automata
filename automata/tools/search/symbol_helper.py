import logging
import os
from typing import Dict, List, Optional, Union

from redbaron import ClassNode, DefNode, RedBaron

from automata.tools.search.local_types import Descriptor, Symbol

logger = logging.getLogger(__name__)


class SymbolHelper:
    PYROOT_NAME = "automata"

    def __init__(self):
        file_dir = os.path.dirname(os.path.abspath(__file__))
        self.repo_abs_path = os.path.join(file_dir, "..", "..")
        self._module_dict = self._build_module_dict()

    def find_and_replace_in_modules(
        self, old_name: str, new_name: str, do_write: bool = True
    ) -> int:
        """
        Renames a function or class in all modules.

        Args:
            old_name (str): The old name of the function or class.
            new_name (str): The new name of the function or class.
        """
        counts = 0
        for module in self._module_dict.values():
            # Find all function or class nodes with the old name
            func_or_class_nodes = module.find_all(("def", "class"), name=old_name)
            counts += str(func_or_class_nodes).count(old_name)
            for node in func_or_class_nodes:
                # Rename the node
                node.name = new_name
            # Find all NameNode's (these could be function calls or variable names)
            name_nodes = module.find_all("name", value=old_name)
            for node in name_nodes:
                # Rename the node
                node.value = new_name
        if do_write:
            self._write_modules()
        return counts

    def find_pattern_in_modules(self, pattern: str) -> Dict[str, List[int]]:
        """
        Finds exact line matches for a given pattern string in all modules.

        Args:
            pattern (str): The pattern string to search for.

        Returns:
            Dict[str, List[int]]: A dictionary with module paths as keys and a list of line numbers as values.
        """
        matches = {}
        for module_path, module in self._module_dict.items():
            lines = str(module).splitlines()
            line_numbers = [i + 1 for i, line in enumerate(lines) if pattern in line.strip()]
            if line_numbers:
                matches[module_path] = line_numbers
        return matches

    def find_fst_object(self, symbol: Symbol) -> Optional[RedBaron]:
        """
        Returns the RedBaron object for the given symbol.

        Args:
            symbol (str): The symbol which corresponds to a module, class, or method.

        Returns:
            Union[ClassNode, DefNode]: The RedBaron FST object for the class or method, or None if not found.
        """

        # Extract the module path, class/method name from the symbol
        descriptors = symbol.descriptors
        obj = None
        while descriptors:
            top_descriptor = descriptors.pop(0)
            if (
                Descriptor.convert_scip_to_python_suffix(top_descriptor)
                == Descriptor.PythonTypes.Module
            ):
                obj = self._find_module(top_descriptor.name.replace(".", os.path.sep) + ".py")
                # TODO - Understand why some modules might be None, like "setup.py"
                if not obj or "test" in top_descriptor.name:
                    return None
            elif (
                Descriptor.convert_scip_to_python_suffix(top_descriptor)
                == Descriptor.PythonTypes.Class
            ):
                if not obj:
                    raise ValueError("Class descriptor found without module descriptor")
                obj = obj.find("class", name=top_descriptor.name)
            elif (
                Descriptor.convert_scip_to_python_suffix(top_descriptor)
                == Descriptor.PythonTypes.Method
            ):
                if not obj:
                    raise ValueError("Method descriptor found without module or class descriptor")
                obj = obj.find("def", name=top_descriptor.name)
        return obj

    def find_return_type(self, fst_object: Union[ClassNode, DefNode]) -> Optional[str]:
        """
        Find the return type for a given function/method symbol's FST object.

        Args:
            fst_object (Union[ClassNode, DefNode]): The FST object for the symbol

        Returns:
            str: The return type of the symbol, or None if not found.
        """
        if isinstance(fst_object, DefNode):
            return_annotation = fst_object.return_annotation
            if return_annotation is not None:
                return return_annotation.dumps().strip()
        return None

    def find_symbol_type(self, symbol: Symbol) -> Optional[str]:
        """
        Check if the given RedBaron node represents a function call.

        :param node: The RedBaron node to check.
        :return: True if the node represents a call, False otherwise.
        """
        node = self.find_fst_object(symbol)
        if node:
            return node.type
        return None

    def _build_module_dict(self) -> Dict[str, RedBaron]:
        """
        Builds the module dictionary by walking through the root directory and creating FST Module objects
        for each Python source file. The module paths are used as keys in the dictionary.

        Returns:
            Dict[str, RedBaron]: A dictionary with module paths as keys and RedBaron objects as values.
        """
        module_dict = {}
        for root, _, files in os.walk(self.repo_abs_path):
            for file in files:
                if file.endswith(".py"):
                    module_path = os.path.join(root, file)
                    module = self._load_module_from_path(module_path)
                    if module:
                        module_rel_path = SymbolHelper._relative_module_path(
                            self.repo_abs_path, module_path
                        )
                        module_dict[module_rel_path] = module
        return module_dict

    def _find_module(self, file_path) -> Optional[RedBaron]:
        """
        Find the FST object for the given file path.

        Args:
            file_path (str): The file path of the Python source code.
        """
        return self._module_dict.get(file_path, None)

    def _write_modules(self):
        """
        Writes all modules back to their source files.
        """
        for module_path, module in self._module_dict.items():
            with open(module_path, "w") as file:
                file.write(module.dumps())

    @staticmethod
    def _load_module_from_path(path: str) -> Optional[RedBaron]:
        """
        Loads and returns an FST object for the given file path.

        Args:
            path (str): The file path of the Python source code.

        Returns:
            Module: RedBaron FST object.
        """

        try:
            module = RedBaron(open(path).read())
            return module
        except Exception as e:
            logger.error(f"Failed to load module '{path}' due to: {e}")
            return None

    @staticmethod
    def _relative_module_path(root_abs_path, module_path):
        module_rel_path = os.path.join(
            SymbolHelper.PYROOT_NAME, os.path.relpath(module_path, root_abs_path)
        )
        return module_rel_path
