import logging
import os.path
from typing import Dict, Iterable, Optional, Tuple

from redbaron import RedBaron

from automata.core.base.patterns.singleton import Singleton
from automata.core.utils import get_root_fpath, get_root_py_fpath

logger = logging.getLogger(__name__)


NO_RESULT_FOUND_STR = "No Result Found."
DOT_SEP = "."


def convert_fpath_to_module_dotpath(root_abs_path: str, module_path: str, prefix: str) -> str:
    """Converts a filepath to a module dotpath"""
    prefix = "" if prefix == "." else f"{prefix}."
    return prefix + (os.path.relpath(module_path, root_abs_path).replace(os.path.sep, "."))[:-3]


class _DotPathMap:
    """A map from module dotpaths to module filepaths"""

    def __init__(self, path: str, prefix: str) -> None:
        """
        Args:
            path: The absolute path to the root of the module tree
            prefix: The prefix to add to the dotpath of each module
        """
        self.prefix = prefix
        self.path = path
        self._module_dotpath_to_fpath_map = self._build_module_dotpath_to_fpath_map()
        self._module_fpath_to_dotpath_map = {
            v: k for k, v in self._module_dotpath_to_fpath_map.items()
        }

    def _build_module_dotpath_to_fpath_map(self) -> Dict[str, str]:
        """Builds a map from module dotpaths to module filepaths"""
        module_dotpath_to_fpath_map = {}
        for root, _, files in os.walk(self.path):
            for file in files:
                if file.endswith(".py"):
                    module_fpath = os.path.join(root, file)
                    module_dotpath = convert_fpath_to_module_dotpath(
                        self.path, module_fpath, self.prefix
                    )
                    module_dotpath_to_fpath_map[module_dotpath] = module_fpath
        return module_dotpath_to_fpath_map

    def get_module_fpath_by_dotpath(self, module_dotpath: str) -> str:
        """Gets the filepath of a module given its dotpath"""
        return self._module_dotpath_to_fpath_map[module_dotpath]

    def get_module_dotpath_by_fpath(self, module_fpath: str) -> str:
        """Gets the dotpath of a module given its filepath"""
        return self._module_fpath_to_dotpath_map[module_fpath]

    def contains_dotpath(self, module_dotpath: str) -> bool:
        return module_dotpath in self._module_dotpath_to_fpath_map

    def contains_fpath(self, module_fpath: str) -> bool:
        return module_fpath in self._module_fpath_to_dotpath_map

    def put_module(self, module_dotpath: str) -> None:
        """
        Puts a module with the given dotpath in the local store

        Raises:
            Exception: If the module already exists in the map
        """
        if self.contains_dotpath(module_dotpath):
            raise Exception(f"Module with dotpath {module_dotpath} already exists!")
        module_os_rel_path = os.path.relpath(
            module_dotpath.replace(DOT_SEP, os.path.sep), self.prefix
        )
        module_os_path = os.path.join(self.path, module_os_rel_path)
        os.makedirs(os.path.dirname(module_os_path), exist_ok=True)
        file_path = f"{module_os_path}.py"
        self._module_dotpath_to_fpath_map[module_dotpath] = file_path
        self._module_fpath_to_dotpath_map[file_path] = module_dotpath

    def items(self) -> Iterable[Tuple[str, str]]:
        """
        Returns:
            A dictionary containing the module dotpath to module filepath mapping
        """
        return self._module_dotpath_to_fpath_map.items()


class PyModuleLoader(metaclass=Singleton):
    """
    A Singleton with a lazy dictionary mapping dotpaths to their corresponding RedBaron FST objects.
    Loads and caches modules in memory as they are accessed

    TODO: Is there a clean way to avoid pasting `_assert_initialized` everywhere?
    TODO: Is there a clean way to remove the type: ignore comments?
          Towards this end a function decorator was also explored, but found to be insufficient.
    """

    initialized = False
    py_fpath: Optional[str] = None
    root_fpath: Optional[str] = None

    _dotpath_map: Optional[_DotPathMap] = None
    _loaded_modules: Dict[str, Optional[RedBaron]] = {}

    def __init__(self) -> None:
        pass

    def initialize(
        self, root_fpath: str = get_root_fpath(), py_fpath: str = get_root_py_fpath()
    ) -> None:
        """
        Initializes the loader by setting paths across the entire project

        Raises:
            Exception: If the map or python directory have already been initialized

        Note:
            root_path should point to the root directory of the project, in the default case this
            might look something like "/Users/me/Automata", root_py_path should point to the root directory
            of the python modules, in the default case this might look something like "/Users/me/Automata/automata"

        """
        path_prefix = os.path.relpath(py_fpath, root_fpath)

        if self.initialized:
            raise Exception("Module loader is already initialized!")

        self._dotpath_map = _DotPathMap(py_fpath, path_prefix)
        self.py_fpath = py_fpath
        self.root_fpath = root_fpath
        self.initialized = True

    def _assert_initialized(self) -> None:
        """
        Checks if the map and python directory have been initialized

        Raises:
            Exception: If the map or python directory have not been initialized
        """
        if not self.initialized:
            raise Exception("Module loader is not yet initialized!")

    def __contains__(self, dotpath: str) -> bool:
        """
        Checks if the map contains a module with the given dotpath

        Raises:
            Exception: If the map or python directory have not been initialized
        """
        self._assert_initialized()
        return self._dotpath_map.contains_dotpath(dotpath)  # type: ignore

    def items(self) -> Iterable[Tuple[str, Optional[RedBaron]]]:
        """
        Returns:
            A dictionary containing the module dotpath to module RedBaron FST object mapping.

        Raises:
            Exception: If the map or python directory have not been initialized.
        """
        self._assert_initialized()
        self._load_all_modules()
        return self._loaded_modules.items()

    def fetch_module(self, module_dotpath: str) -> Optional[RedBaron]:
        """
        Gets the module with the given dotpath.

        Raises:
            Exception: If the map or python directory have not been initialized
        """
        self._assert_initialized()
        if not self._dotpath_map.contains_dotpath(module_dotpath):  # type: ignore
            return None

        if module_dotpath not in self._loaded_modules:
            module_fpath = self._dotpath_map.get_module_fpath_by_dotpath(module_dotpath)  # type: ignore
            self._loaded_modules[module_dotpath] = self._load_module_from_fpath(module_fpath)
        return self._loaded_modules[module_dotpath]

    def fetch_existing_module_dotpath(self, module_obj: RedBaron) -> Optional[str]:
        """
        Gets the module dotpath for the specified module object.

        Args:
            module_obj (Module): The module object.

        Returns:
            str: The module dotpath for the specified module object.

        Raises:
            Exception: If the map or python directory have not been initialized
        """
        self._assert_initialized()
        return next(
            (
                module_dotpath
                for module_dotpath, module in self._loaded_modules.items()
                if module == module_obj
            ),
            None,
        )

    def fetch_existing_module_fpath_by_dotpath(self, module_dotpath: str) -> Optional[str]:
        """
        Gets the module fpath for the specified module dotpath.

        Args:
            module_dotpath (str): The module dotpath.

        Returns:
            str: The module fpath for the specified module dotpath.

        Raises:
            Exception: If the map or python directory have not been initialized
        """
        self._assert_initialized()
        if module_dotpath in self._loaded_modules:
            return self._dotpath_map.get_module_fpath_by_dotpath(module_dotpath)  # type: ignore
        return None

    def get_module_dotpath_by_fpath(self, module_fpath: str) -> str:
        """
        Gets the module dotpath for the specified module fpath.

        Args:
            module_fpath (str): The module fpath.

        Returns:
            str: The module dotpath for the specified module fpath.

        Raises:
            Exception: If the map or python directory have not been initialized
        """
        self._assert_initialized()
        return self._dotpath_map.get_module_dotpath_by_fpath(module_fpath)  # type: ignore

    def put_module(self, module_dotpath: str, module: RedBaron) -> None:
        """
        Put a module with the given dotpath in the map

        Args:
            module_dotpath: The dotpath of the module
            module: The module to put in the map

        Raises:
            Exception: If the map or python directory have not been initialized
        """
        self._assert_initialized()
        self._loaded_modules[module_dotpath] = module
        self._dotpath_map.put_module(module_dotpath)  # type: ignore

    def _load_all_modules(self) -> None:
        """
        Loads all modules in the map

        Raises:
            Exception: If the map or python directory have not been initialized
        """
        for module_dotpath, fpath in self._dotpath_map.items():  # type: ignore
            if (
                not self.py_fpath
                or self.py_fpath not in module_dotpath
                or "tasks" in module_dotpath
            ):
                continue
            if module_dotpath not in self._loaded_modules:
                self._loaded_modules[module_dotpath] = self._load_module_from_fpath(fpath)

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
            return RedBaron(open(path).read())
        except Exception as e:
            logger.error(f"Failed to load module '{path}' due to: {e}")
            return None


py_module_loader = PyModuleLoader()
