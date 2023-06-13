import ast
import os
from _ast import AsyncFunctionDef, ClassDef, FunctionDef

NO_RESULT_FOUND_STR = "No Result Found."
DOT_SEP = "."


def convert_fpath_to_module_dotpath(root_abs_path, module_path):
    module_rel_path = (os.path.relpath(module_path, root_abs_path).replace(os.path.sep, "."))[:-3]
    return module_rel_path


def build_repository_overview(path: str, skip_test: bool = True, skip_func=False) -> str:
    """
    Loops over the directory python files and returns a string that provides an overview of the PythonParser's state.
    Returns:
        str: A string that provides an overview of the PythonParser's state.
    **NOTE: This method uses AST, not RedBaron, because RedBaron initialization is slow and unnecessary for this method.
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


def _overview_traverse_helper(node, line_items, skip_func=False, num_spaces=1):
    if isinstance(node, ClassDef):
        line_items.append("  " * num_spaces + " - cls " + node.name)
    elif (isinstance(node, FunctionDef) or isinstance(node, AsyncFunctionDef)) and not skip_func:
        line_items.append("  " * num_spaces + " - func " + node.name)

    for child in ast.iter_child_nodes(node):
        _overview_traverse_helper(child, line_items, skip_func, num_spaces + 1)
