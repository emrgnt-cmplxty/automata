from typing import Dict, List

from automata.tools.search.symbol_converter import SymbolConverter
from automata.tools.search.symbol_types import Descriptor, Symbol


def get_rankable_symbols(
    symbols: List[Symbol],
    filter_strings=["setup", "local", "stdlib", "redbaron"],  # "test", "__init__",
    accepted_kinds=[Descriptor.PythonKinds.Method, Descriptor.PythonKinds.Class],
) -> List[Symbol]:
    """
    Filter out symbols that are not relevant for the embedding map.

    Args:
        symbols: List of symbols to filter
    Returns:
        List of filtered symbols
    """
    filtered_symbols = []

    for symbol in symbols:
        do_continue = False
        for filter_string in filter_strings:
            if filter_string in symbol.uri:
                do_continue = True
                break
        if do_continue:
            continue

        symbol_kind = symbol.symbol_kind_by_suffix()
        if symbol_kind not in accepted_kinds:
            continue
        filtered_symbols.append(symbol)
    return filtered_symbols


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
