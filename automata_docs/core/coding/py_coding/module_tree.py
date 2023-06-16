import logging
import os.path
from functools import lru_cache
from typing import Dict, Iterable, Optional, Tuple

from redbaron import RedBaron

from automata_docs.core.coding.py_coding.py_utils import (
    DOT_SEP,
    convert_fpath_to_module_dotpath,
)
from automata_docs.core.utils import root_fpath

logger = logging.getLogger(__name__)


class DotPathMap:
    """A map from module dotpaths to module filepaths"""

    def __init__(self, path: str):
        """
        Args:
            path: The absolute path to the root of the module tree
        """
        if not os.path.isabs(path):
            path = os.path.join(root_fpath(), path)
        self._abs_path = path
        self._module_dotpath_to_fpath_map = self._build_module_dotpath_to_fpath_map()
        self._module_fpath_to_dotpath_map = {
            v: k for k, v in self._module_dotpath_to_fpath_map.items()
        }

    def _build_module_dotpath_to_fpath_map(self) -> Dict[str, str]:
        """
        Builds a map from module dotpaths to module filepaths

        Returns:
            The map from module dotpaths to module filepaths
        """
        module_dotpath_to_fpath_map = {}
        for root, _, files in os.walk(self._abs_path):
            for file in files:
                if file.endswith(".py"):
                    module_fpath = os.path.join(root, file)
                    module_dotpath = convert_fpath_to_module_dotpath(self._abs_path, module_fpath)
                    module_dotpath_to_fpath_map[module_dotpath] = module_fpath
        return module_dotpath_to_fpath_map

    def get_module_fpath_by_dotpath(self, module_dotpath: str) -> str:
        """
        Gets the filepath of a module given its dotpath

        Args:
            module_dotpath: The dotpath of the module

        Returns:
            The filepath of the module
        """
        return self._module_dotpath_to_fpath_map[module_dotpath]

    def get_module_dotpath_by_fpath(self, module_fpath: str) -> str:
        """
        Gets the dotpath of a module given its filepath

        Args:
            module_fpath: The filepath of the module

        Returns:
            The dotpath of the module
        """
        return self._module_fpath_to_dotpath_map[module_fpath]

    def contains_dotpath(self, module_dotpath: str) -> bool:
        """
        Checks if the map contains a module with the given dotpath

        Args:
            module_dotpath: The dotpath of the module

        Returns:
            True if the map contains the module, False otherwise
        """
        return module_dotpath in self._module_dotpath_to_fpath_map

    def contains_fpath(self, module_fpath: str) -> bool:
        """
        Checks if the map contains a module with the given filepath

        Args:
            module_fpath: The filepath of the module

        Returns:
            True if the map contains the module, False otherwise
        """
        return module_fpath in self._module_fpath_to_dotpath_map

    def put_module(self, module_dotpath: str):
        """
        Puts a module with the given dotpath in the map

        Args:
            module_dotpath: The dotpath of the module
        """
        if not self.contains_dotpath(module_dotpath):
            module_os_rel_path = module_dotpath.replace(DOT_SEP, os.path.sep)
            module_os_abs_path = os.path.join(self._abs_path, module_os_rel_path)
            os.makedirs(os.path.dirname(module_os_abs_path), exist_ok=True)
            file_path = f"{module_os_abs_path}.py"
            self._module_dotpath_to_fpath_map[module_dotpath] = file_path
            self._module_fpath_to_dotpath_map[file_path] = module_dotpath

    def items(self) -> Iterable[Tuple[str, str]]:
        """
        Returns:
            A dictionary containing the module dotpath to module filepath mapping
        """
        return self._module_dotpath_to_fpath_map.items()


class LazyModuleTreeMap:
    """
    A lazy dictionary between module dotpaths and their corresponding RedBaron FST objects.
    Loads and caches modules in memory as they are accessed
    """

    def __init__(self, path: str):
        """
        Args:
            path: The absolute path to the root of the module tree
        """
        self._dotpath_map = DotPathMap(path)
        self._loaded_modules: Dict[str, Optional[RedBaron]] = {}

    def __contains__(self, dotpath):
        """
        Checks if the map contains a module with the given dotpath

        Args:
            dotpath: The dotpath of the module
        """
        return self._dotpath_map.contains_dotpath(dotpath)

    def items(self) -> Iterable[Tuple[str, Optional[RedBaron]]]:
        """
        Returns:
            A dictionary containing the module dotpath to module RedBaron FST object mapping
        """
        self._load_all_modules()
        return self._loaded_modules.items()

    def fetch_module(self, module_dotpath: str) -> Optional[RedBaron]:
        """
        Gets the module with the given dotpath

        Args:
            module_dotpath: The dotpath of the module

        Returns:
            Optional[RedBaron]: The module with the given dotpath if found, None otherwise
        """
        if not self._dotpath_map.contains_dotpath(module_dotpath):
            return None

        if module_dotpath not in self._loaded_modules:
            module_fpath = self._dotpath_map.get_module_fpath_by_dotpath(module_dotpath)
            self._loaded_modules[module_dotpath] = self._load_module_from_fpath(module_fpath)
        return self._loaded_modules[module_dotpath]

    def fetch_existing_module_dotpath(self, module_obj: RedBaron) -> Optional[str]:
        """
        Gets the module dotpath for the specified module object.

        Args:
            module_obj (Module): The module object.

        Returns:
            str: The module dotpath for the specified module object.
        """
        # there is no way a module that has a redbaron object is not loaded
        for module_dotpath, module in self._loaded_modules.items():
            if module == module_obj:
                return module_dotpath
        return None

    def fetch_existing_module_fpath_by_dotpath(self, module_dotpath: str) -> Optional[str]:
        """
        Gets the module fpath for the specified module dotpath.

        Args:
            module_dotpath (str): The module dotpath.

        Returns:
            str: The module fpath for the specified module dotpath.
        """

        if module_dotpath in self._loaded_modules:
            return self._dotpath_map.get_module_fpath_by_dotpath(module_dotpath)
        return None

    def get_module_dotpath_by_fpath(self, module_fpath: str) -> str:
        """
        Gets the module dotpath for the specified module fpath.

        Args:
            module_fpath (str): The module fpath.
        """
        return self._dotpath_map.get_module_dotpath_by_fpath(module_fpath)

    def put_module(self, module_dotpath: str, module: RedBaron):
        """
        Put a module with the given dotpath in the map

        Args:
            module_dotpath: The dotpath of the module
            module: The module to put in the map
        """
        self._loaded_modules[module_dotpath] = module
        self._dotpath_map.put_module(module_dotpath)

    def _load_all_modules(self):
        """Loads all modules in the map"""
        for module_dotpath, fpath in self._dotpath_map.items():
            if module_dotpath not in self._loaded_modules:
                self._loaded_modules[module_dotpath] = self._load_module_from_fpath(fpath)

    @classmethod
    @lru_cache(maxsize=1)
    def cached_default(cls) -> "LazyModuleTreeMap":
        """Creates a new LazyModuleTreeMap instance with the default root path"""
        return cls(root_fpath())

    @staticmethod
    def _load_module_from_fpath(path: str) -> Optional[RedBaron]:
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
