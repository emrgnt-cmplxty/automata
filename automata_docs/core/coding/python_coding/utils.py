import ast
import os
from _ast import AsyncFunctionDef, ClassDef, FunctionDef
from typing import List

from redbaron import RedBaron

NO_RESULT_FOUND_STR = "No Result Found."
DOT_SEP = "."


def convert_fpath_to_module_dotpath(root_abs_path: str, module_path: str) -> str:
    """
    Converts a filepath to a module dotpath

    Args:
        root_abs_path: The absolute path of the root directory
        module_path: The path of the module

    Returns:
        The dotpath of the module
    """
    module_rel_path = (os.path.relpath(module_path, root_abs_path).replace(os.path.sep, "."))[:-3]
    return module_rel_path


def build_repository_overview(path: str, skip_test: bool = True, skip_func: bool = False) -> str:
    """
    Builds an overview of the repository below the specified path

    Args:
        path: The path to the root of the repository
        skip_test: Whether or not to skip test files
        skip_func: Whether or not to skip function definitions
    Returns:
        str: A string that provides an overview beneath the specified path

    NOTE: This method uses AST, not RedBaron, because RedBaron
        initialization is slow and unnecessary for this method.
    TODO: Move to redbaron for consistency
    """
    result_lines = []
    for root, _, files in os.walk(path):
        for file in files:
            if "test" in file and skip_test:
                continue
            if file.endswith(".py"):
                module_path = os.path.join(root, file)
                module = ast.parse(open(module_path).read())
                relative_module_path = convert_fpath_to_module_dotpath(path, module_path)
                result_lines.append(relative_module_path)
                _overview_traverse_helper(module, result_lines, skip_func)
    return "\n".join(result_lines)


def _overview_traverse_helper(
    node: RedBaron, line_items: List[str], skip_func: bool = False, num_spaces: int = 1
):
    """
    Helper method for build_repository_overview

    Args:
        node: The current node in the AST
        line_items: The list of lines to add to
        skip_func: Whether or not to skip function definitions
        num_spaces: The number of spaces to indent
    """

    if isinstance(node, ClassDef):
        line_items.append("  " * num_spaces + " - cls " + node.name)
    elif (isinstance(node, FunctionDef) or isinstance(node, AsyncFunctionDef)) and not skip_func:
        line_items.append("  " * num_spaces + " - func " + node.name)

    for child in ast.iter_child_nodes(node):
        _overview_traverse_helper(child, line_items, skip_func, num_spaces + 1)
