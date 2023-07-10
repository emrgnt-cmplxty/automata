from automata.core.utils import get_root_fpath
from automata.singletons.py_module_loader import py_module_loader


def initialize_modules(*args, **kwargs) -> None:
    root_path = kwargs.get("project_root_fpath") or get_root_fpath()
    project_name = kwargs.get("project_name") or "automata"
    rel_py_path = kwargs.get("project_rel_py_path") or project_name
    py_module_loader.initialize(root_path, rel_py_path)
