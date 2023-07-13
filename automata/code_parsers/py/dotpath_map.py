import os.path
from typing import Dict, Iterable, Tuple


def convert_fpath_to_module_dotpath(
    root_abs_path: str, module_path: str, prefix: str
) -> str:
    """Converts a filepath to a module dotpath"""
    prefix = "" if prefix == "." else f"{prefix}."
    return (
        prefix
        + (
            os.path.relpath(module_path, root_abs_path).replace(
                os.path.sep, "."
            )
        )[:-3]
    )


class DotPathMap:
    """A map from module dotpaths to module filepaths"""

    DOT_SEP = "."

    def __init__(self, path: str, rel_py_path: str) -> None:
        """
        Args:
            path: The absolute path to the root of the module tree
            prefix: The prefix to add to the dotpath of each module
        """
        # TODO - Test that rel_py_path works when path != local directory name
        self.prefix = rel_py_path.replace(os.pathsep, DotPathMap.DOT_SEP)
        # Remove ending '.' in module fpath
        if self.prefix.endswith(DotPathMap.DOT_SEP):
            self.prefix = self.prefix[:-1]
        self.path = path
        self._module_dotpath_to_fpath_map = (
            self._build_module_dotpath_to_fpath_map()
        )
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
            raise Exception(
                f"Module with dotpath {module_dotpath} already exists!"
            )
        module_os_rel_path = os.path.relpath(
            module_dotpath.replace(DotPathMap.DOT_SEP, os.path.sep),
            self.prefix,
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
