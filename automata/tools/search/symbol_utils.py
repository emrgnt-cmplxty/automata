from typing import Dict, List

from automata.tools.search.symbol_converter import SymbolConverter


def find_and_replace_in_modules(
    converter: SymbolConverter, old_name: str, new_name: str, do_write: bool = True
) -> int:
    """
    Renames a function or class in all modules.
    Args:
        old_name (str): The old name of the function or class.
        new_name (str): The new name of the function or class.
    """
    counts = 0
    for module in converter._module_dict.values():
        # Find all function or class nodes with the old name
        func_or_class_nodes = module.find_all(("def", "class"), name=old_name)
        counts += str(func_or_class_nodes).count(old_name)
        for node in func_or_class_nodes:
            # Rename the node
            node.name = new_name
        # Find all NameNode's (these could be function calls or variable names)
        name_nodes = module.find_all("name", value=old_name)
        for node in name_nodes:
            # Rename the node
            node.value = new_name
    if do_write:
        converter._write_modules()
    return counts

def find_pattern_in_modules(converter: SymbolConverter, pattern: str) -> Dict[str, List[int]]:
    """
    Finds exact line matches for a given pattern string in all modules.
    Args:
        pattern (str): The pattern string to search for.
    Returns:
        Dict[str, List[int]]: A dictionary with module paths as keys and a list of line numbers as values.
    """
    matches = {}
    for module_path, module in converter._module_dict.items():
        lines = str(module).splitlines()
        line_numbers = [i + 1 for i, line in enumerate(lines) if pattern in line.strip()]
        if line_numbers:
            matches[module_path] = line_numbers
    return matches