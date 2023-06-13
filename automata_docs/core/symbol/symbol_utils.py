from typing import List, Optional

from redbaron import RedBaron

from automata_docs.core.indexing.python_indexing.module_tree_map import LazyModuleTreeMap
from automata_docs.core.symbol.symbol_types import Symbol, SymbolDescriptor


def convert_to_fst_object(
    symbol: Symbol, module_map: Optional[LazyModuleTreeMap] = None
) -> RedBaron:
    """
    Returns the RedBaron object for the given symbol.
    Args:
        symbol (str): The symbol which corresponds to a module, class, or method.
        module_map: The PythonASTIndexer to use to find the symbol.
    Returns:
        Union[ClassNode, DefNode]: The RedBaron FST object for the class or method, or None if not found.
    Note:
        The optional argument is to allow us to run this function in mulitprocessing in the future,
        because module map is not picklable (because redbaron objects are not picklable)
        So the indexer would have to be created and destroyed in each process.
    """

    # Extract the module path, class/method name from the symbol
    descriptors = list(symbol.descriptors)
    obj = None
    module_map = module_map or LazyModuleTreeMap.cached_default()
    # print('descriptors = ', descriptors)
    # print('module_map._dotpath_map = ', module_map._dotpath_map)
    # print('module_map._dotpath_map._module_dotpath_to_fpath_map = ', module_map._dotpath_map._module_dotpath_to_fpath_map)
    # print('module_map._loaded_modules = ', module_map._loaded_modules)
    while descriptors:
        top_descriptor = descriptors.pop(0)
        if (
            SymbolDescriptor.convert_scip_to_python_suffix(top_descriptor.suffix)
            == SymbolDescriptor.PythonKinds.Module
        ):
            module_dotpath = top_descriptor.name
            if module_dotpath.startswith(""):
                module_dotpath = module_dotpath[len("") :]  # indexer omits this
            obj = module_map.get_module(module_dotpath)
            # TODO - Understand why some modules might be None
            if not obj:
                raise ValueError(f"Module descriptor {top_descriptor.name} not found")
        elif (
            SymbolDescriptor.convert_scip_to_python_suffix(top_descriptor.suffix)
            == SymbolDescriptor.PythonKinds.Class
        ):
            if not obj:
                raise ValueError("Class descriptor found without module descriptor")
            obj = obj.find("class", name=top_descriptor.name)
        elif (
            SymbolDescriptor.convert_scip_to_python_suffix(top_descriptor.suffix)
            == SymbolDescriptor.PythonKinds.Method
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
    ),  # TODO - Revisit what strings we should filter on.
    accepted_kinds=(SymbolDescriptor.PythonKinds.Method, SymbolDescriptor.PythonKinds.Class),
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
