import logging
import os
from typing import Dict, Optional, Union

from redbaron import ClassNode, DefNode, RedBaron

logger = logging.getLogger(__name__)


class SymbolConverter:
    PYROOT_NAME = "automata"

    def __init__(self):
        file_dir = os.path.dirname(os.path.abspath(__file__))
        self.repo_abs_path = os.path.join(file_dir, "..", "..")
        self._module_dict = self._build_module_dict()

    def get_fst_node(self, module: str, line_number: int, column_number: int) -> RedBaron:
        """
        Returns the RedBaron object for the given symbol.
        Args:
            symbol (str): The symbol which corresponds to a module, class, or method.
        Returns:
            Union[ClassNode, DefNode]: The RedBaron FST object for the class or method, or None if not found.
        """
        return self._module_dict[module].find_by_position((line_number, column_number))

    def find_return_type(self, fst_object: Union[RedBaron, ClassNode, DefNode]) -> Optional[str]:
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
                        module_rel_path = SymbolConverter._relative_module_path(
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
            SymbolConverter.PYROOT_NAME, os.path.relpath(module_path, root_abs_path)
        )
        return module_rel_path
