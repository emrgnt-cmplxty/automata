import logging
import os
from copy import deepcopy
from typing import Dict, Optional

from redbaron import RedBaron

from automata.tools.search.symbol_types import Descriptor, Symbol

logger = logging.getLogger(__name__)


class SymbolConverter:
    PYROOT_NAME = "automata"

    def __init__(self):
        file_dir = os.path.dirname(os.path.abspath(__file__))
        self.repo_abs_path = os.path.join(file_dir, "..", "..")
        self._module_dict = self._build_module_dict()

    def convert_to_fst_object(self, symbol: Symbol) -> RedBaron:
        """
        Returns the RedBaron object for the given symbol.
        Args:
            symbol (str): The symbol which corresponds to a module, class, or method.
        Returns:
            Union[ClassNode, DefNode]: The RedBaron FST object for the class or method, or None if not found.
        """

        # Extract the module path, class/method name from the symbol
        descriptors = deepcopy(list(symbol.descriptors))
        obj = None

        while descriptors:
            top_descriptor = descriptors.pop(0)
            if (
                Descriptor.convert_scip_to_python_suffix(top_descriptor.suffix)
                == Descriptor.PythonKinds.Module
            ):
                obj = self._find_module(top_descriptor.name.replace(".", os.path.sep) + ".py")
                # TODO - Understand why some modules might be None
                if not obj or "test" in top_descriptor.name:
                    raise ValueError(f"Module descriptor {top_descriptor.name} not found")
            elif (
                Descriptor.convert_scip_to_python_suffix(top_descriptor.suffix)
                == Descriptor.PythonKinds.Class
            ):
                if not obj:
                    raise ValueError("Class descriptor found without module descriptor")
                obj = obj.find("class", name=top_descriptor.name)
            elif (
                Descriptor.convert_scip_to_python_suffix(top_descriptor.suffix)
                == Descriptor.PythonKinds.Method
            ):
                if not obj:
                    raise ValueError("Method descriptor found without module or class descriptor")
                obj = obj.find("def", name=top_descriptor.name)
        if not obj:
            raise ValueError(f"Symbol {symbol} not found")
        return obj

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
