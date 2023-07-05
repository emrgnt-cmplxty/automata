from typing import List

from redbaron import RedBaron

from automata.core.singletons.py_module_loader import py_module_loader
from automata.core.symbol.base import Symbol, SymbolDescriptor


def convert_to_fst_object(symbol: Symbol) -> RedBaron:
    """
    Converts a specified symbol into it's corresponding RedBaron FST object

    Raises:
        ValueError: If the symbol is not found
    """
    # Extract the module path, class/method name from the symbol
    descriptors = list(symbol.descriptors)
    obj = None
    while descriptors:
        top_descriptor = descriptors.pop(0)
        if (
            SymbolDescriptor.convert_scip_to_python_suffix(top_descriptor.suffix)
            == SymbolDescriptor.PyKind.Module
        ):
            module_dotpath = top_descriptor.name
            if module_dotpath.startswith(""):
                module_dotpath = module_dotpath[len("") :]  # indexer omits this
            obj = py_module_loader.fetch_module(module_dotpath)
            # TODO - Understand why some modules might be None
            if not obj:
                raise ValueError(f"Module descriptor {top_descriptor.name} not found")
        elif (
            SymbolDescriptor.convert_scip_to_python_suffix(top_descriptor.suffix)
            == SymbolDescriptor.PyKind.Class
        ):
            if not obj:
                raise ValueError("Class descriptor found without module descriptor")
            obj = obj.find("class", name=top_descriptor.name)
        elif (
            SymbolDescriptor.convert_scip_to_python_suffix(top_descriptor.suffix)
            == SymbolDescriptor.PyKind.Method
        ):
            if not obj:
                raise ValueError("Method descriptor found without module or class descriptor")
            obj = obj.find("def", name=top_descriptor.name)
    if not obj:
        raise ValueError(f"Symbol {symbol} not found")
    return obj


def get_rankable_symbols(
    symbols: List[Symbol],
    filter_strings=(
        "setup",
        "stdlib",
    ),
    accepted_kinds=(SymbolDescriptor.PyKind.Method, SymbolDescriptor.PyKind.Class),
) -> List[Symbol]:
    """
    Get a list of Symbols which are supported by SymbolRank.


    TODO - Revisit filtering logic
    """
    filtered_symbols = []

    for symbol in symbols:
        do_continue = any(filter_string in symbol.uri for filter_string in filter_strings)
        if do_continue:
            continue

        symbol_kind = symbol.symbol_kind_by_suffix()
        if symbol_kind not in accepted_kinds:
            continue
        if (
            Symbol.is_protobuf(symbol)
            or Symbol.is_local(symbol)
            or Symbol.is_meta(symbol)
            or Symbol.is_parameter(symbol)
        ):
            continue

        filtered_symbols.append(symbol)
    return filtered_symbols
