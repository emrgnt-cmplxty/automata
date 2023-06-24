import logging
import os.path
from typing import Dict, Iterable, Optional, Tuple

from redbaron import RedBaron

from automata.core.base.singleton import Singleton
from automata.core.coding.py.py_utils import DOT_SEP, convert_fpath_to_module_dotpath
from automata.core.utils import root_fpath, root_py_fpath

logger = logging.getLogger(__name__)


class _DotPathMap:
    """A map from module dotpaths to module filepaths"""

    def __init__(self, path: str) -> None:
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

    def put_module(self, module_dotpath: str) -> None:
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


class ModuleLoader(Singleton):
    """
    A lazy dictionary between module dotpaths and their corresponding RedBaron FST objects.
    Loads and caches modules in memory as they are accessed

    TODO: Defaulting 'py_dir' to automata for now and then introducing smarter
           logic to infer the py_dir from the path later

    TODO: Is there a clean way to avoid pasting `_assert_initialized` everywhere?
    TODO: Is there a clean way to remove the type: ignore comments?
          Towards this end a function decorator was also explored, but found to be insufficient.
    """

    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ModuleLoader, cls).__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if self._initialized:
            return
        self._dotpath_map: Optional[_DotPathMap] = None
        self.py_dir: Optional[str] = None
        self._loaded_modules: Dict[str, Optional[RedBaron]] = {}
        self._initialized = True

    def set_paths(self, path: str = root_py_fpath(), py_dir: Optional[str] = None) -> None:
        if self._dotpath_map is not None:
            raise Exception("Paths already set!")
        if self.py_dir is not None:
            raise Exception("PyDir already set!")
        self._dotpath_map = _DotPathMap(path)
        if not py_dir:
            py_dir = path.split(os.pathsep)[-1]
        self.py_dir = py_dir

    def _assert_initialized(self) -> None:
        """
        Checks if the map and python directory have been initialized

        Raises:
            Exception: If the map or python directory have not been initialized
        """
        if self._dotpath_map is None:
            raise Exception("Paths not set!")
        if self.py_dir is None:
            raise Exception("PyDir not set!")

    def __contains__(self, dotpath: str) -> bool:
        """
        Checks if the map contains a module with the given dotpath

        Args:
            dotpath: The dotpath of the module

        Returns:
            True if the map contains the module, False otherwise

        Raises:
            Exception: If the map or python directory have not been initialized
        """
        self._assert_initialized()
        return self._dotpath_map.contains_dotpath(dotpath)  # type: ignore

    def items(self) -> Iterable[Tuple[str, Optional[RedBaron]]]:
        """
        Returns:
            A dictionary containing the module dotpath to module RedBaron FST object mapping

        Raises:
            Exception: If the map or python directory have not been initialized
        """
        self._assert_initialized()
        self._load_all_modules()
        return self._loaded_modules.items()

    def fetch_module(self, module_dotpath: str) -> Optional[RedBaron]:
        """
        Gets the module with the given dotpath

        Args:
            module_dotpath: The dotpath of the module

        Returns:
            Optional[RedBaron]: The module with the given dotpath if found, None otherwise

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
        FIXME: Filter on py_dir for now and then introduce smarter logic later
        """
        for module_dotpath, fpath in self._dotpath_map.items():  # type: ignore
            if self.py_dir not in module_dotpath or "tasks" in module_dotpath:
                continue
            print("loading dotpath = ", module_dotpath)
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
