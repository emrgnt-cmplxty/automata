import ast
from typing import List, Optional

from automata.singletons.py_module_loader import py_module_loader

from .symbol_base import Symbol, SymbolDescriptor


def convert_to_ast_object(symbol: Symbol) -> ast.AST:
    """
    Converts a specified symbol into it's corresponding ast.AST object

    Raises:
        ValueError: If the symbol is not found
    """
    descriptors = list(symbol.descriptors)
    obj: Optional[ast.AST] = None
    while descriptors:
        top_descriptor = descriptors.pop(0)
        if (
            SymbolDescriptor.convert_scip_to_python_kind(top_descriptor.suffix)
            == SymbolDescriptor.PyKind.Module
        ):
            module_path = top_descriptor.name
            if module_path.startswith(""):
                module_path = module_path[len("") :]  # indexer omits this
            module_dotpath = top_descriptor.name
            if module_dotpath.startswith(""):
                module_dotpath = module_dotpath[
                    len("") :
                ]  # indexer omits this
            obj = py_module_loader.fetch_ast_module(module_dotpath)
            if not obj:
                raise ValueError(f"Module {module_dotpath} not found")
        elif (
            SymbolDescriptor.convert_scip_to_python_kind(top_descriptor.suffix)
            == SymbolDescriptor.PyKind.Class
        ):
            if not obj:
                raise ValueError(
                    "Class descriptor found without module descriptor"
                )
            obj = next(
                (
                    node
                    for node in ast.walk(obj)
                    if isinstance(node, ast.ClassDef)
                    and node.name == top_descriptor.name
                ),
                None,
            )
        elif (
            SymbolDescriptor.convert_scip_to_python_kind(top_descriptor.suffix)
            == SymbolDescriptor.PyKind.Method
        ):
            if not obj:
                raise ValueError(
                    "Method descriptor found without module or class descriptor"
                )
            obj = next(
                (
                    node
                    for node in ast.walk(obj)
                    if isinstance(
                        node, (ast.FunctionDef, ast.AsyncFunctionDef)
                    )
                    and node.name == top_descriptor.name
                ),
                None,
            )
    if not obj:
        raise ValueError(f"Symbol {symbol} not found")
    return obj


def get_rankable_symbols(
    symbols: List[Symbol],
    symbols_strings_to_filter: List[str] = [
        "setup",
        "stdlib",
    ],
    accepted_kinds=(
        SymbolDescriptor.PyKind.Method,
        SymbolDescriptor.PyKind.Class,
    ),
) -> List[Symbol]:
    """
    Get a list of Symbols which are supported by SymbolRank.


    TODO - Revisit filtering logic
    """
    filtered_symbols = []

    for symbol in symbols:
        do_continue = any(
            filter_string in symbol.uri
            for filter_string in symbols_strings_to_filter
        )
        if do_continue:
            continue

        if symbol.py_kind not in accepted_kinds:
            continue
        if (
            symbol.is_protobuf
            or symbol.is_local
            or symbol.is_meta
            or symbol.is_parameter
        ):
            continue

        filtered_symbols.append(symbol)
    return filtered_symbols
