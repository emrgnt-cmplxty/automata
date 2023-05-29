import logging
import os.path
from functools import lru_cache
from typing import Dict, Optional

from redbaron import RedBaron

from automata.core.code_indexing.utils import DOT_SEP, convert_fpath_to_module_dotpath
from automata.core.utils import root_path, root_py_path

logger = logging.getLogger(__name__)


class DotPathMap:
    def __init__(self, path: str):
        if not os.path.isabs(path):
            path = os.path.join(root_path(), path)
        self._abs_path = path
        self._module_dotpath_to_fpath_map = self._build_module_dotpath_to_fpath_map()
        self._module_fpath_to_dotpath_map = {
            v: k for k, v in self._module_dotpath_to_fpath_map.items()
        }

    def _build_module_dotpath_to_fpath_map(self) -> Dict[str, str]:
        module_dotpath_to_fpath_map = {}
        for root, _, files in os.walk(self._abs_path):
            for file in files:
                if file.endswith(".py"):
                    module_fpath = os.path.join(root, file)
                    module_dotpath = convert_fpath_to_module_dotpath(self._abs_path, module_fpath)
                    module_dotpath_to_fpath_map[module_dotpath] = module_fpath
        return module_dotpath_to_fpath_map

    def get_module_fpath_by_dotpath(self, module_dotpath: str) -> str:
        return self._module_dotpath_to_fpath_map[module_dotpath]

    def get_module_dotpath_by_fpath(self, module_fpath: str) -> str:
        return self._module_fpath_to_dotpath_map[module_fpath]

    def contains_dotpath(self, module_dotpath: str) -> bool:
        return module_dotpath in self._module_dotpath_to_fpath_map

    def contains_fpath(self, module_fpath: str) -> bool:
        return module_fpath in self._module_fpath_to_dotpath_map

    def put_module(self, module_dotpath: str):
        if not self.contains_dotpath(module_dotpath):
            module_os_rel_path = module_dotpath.replace(DOT_SEP, os.path.sep)
            module_os_abs_path = os.path.join(self._abs_path, module_os_rel_path)
            os.makedirs(os.path.dirname(module_os_abs_path), exist_ok=True)
            file_path = f"{module_os_abs_path}.py"
            self._module_dotpath_to_fpath_map[module_dotpath] = file_path
            self._module_fpath_to_dotpath_map[file_path] = module_dotpath

    def items(self):
        return self._module_dotpath_to_fpath_map.items()


class LazyModuleTreeMap:
    """
    This map works as a lazy dictionary between module dotpaths and their corresponding RedBaron FST objects.
    It will load and cache modules in memory as they get accessed
    """

    def __init__(self, path: str):
        self._dotpath_map = DotPathMap(path)
        self._loaded_modules: Dict[str, Optional[RedBaron]] = {}

    def get_module(self, module_dotpath: str) -> Optional[RedBaron]:
        if not self._dotpath_map.contains_dotpath(module_dotpath):
            return None

        if module_dotpath not in self._loaded_modules:
            module_fpath = self._dotpath_map.get_module_fpath_by_dotpath(module_dotpath)
            self._loaded_modules[module_dotpath] = self._load_module_from_fpath(module_fpath)
        return self._loaded_modules[module_dotpath]

    def put_module(self, module_dotpath: str, module: RedBaron):
        self._loaded_modules[module_dotpath] = module
        self._dotpath_map.put_module(module_dotpath)

    @staticmethod
    def _load_module_from_fpath(path) -> Optional[RedBaron]:
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

    def get_existing_module_dotpath(self, module_obj: RedBaron) -> Optional[str]:
        """
        Returns the module dotpath for the specified module object.

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

    def get_existing_module_fpath_by_dotpath(self, module_dotpath: str) -> Optional[str]:
        """
        Returns the module fpath for the specified module dotpath.

        Args:
            module_dotpath (str): The module dotpath.

        Returns:
            str: The module fpath for the specified module dotpath.
        """

        if module_dotpath in self._loaded_modules:
            return self._dotpath_map.get_module_fpath_by_dotpath(module_dotpath)
        return None

    def get_module_dotpath_by_fpath(self, module_fpath: str) -> str:
        return self._dotpath_map.get_module_dotpath_by_fpath(module_fpath)

    def items(self):
        self._load_all_modules()
        return self._loaded_modules.items()

    def _load_all_modules(self):
        for module_dotpath, fpath in self._dotpath_map.items():
            if module_dotpath not in self._loaded_modules:
                self._loaded_modules[module_dotpath] = self._load_module_from_fpath(fpath)

    def __contains__(self, item):
        return self._dotpath_map.contains_dotpath(item)

    @classmethod
    @lru_cache(maxsize=1)
    def cached_default(cls) -> "LazyModuleTreeMap":
        return cls(root_py_path())
