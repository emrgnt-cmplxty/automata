from ast import AST, AsyncFunctionDef, ClassDef, FunctionDef, Module, iter_child_nodes
from ast import parse as pyast_parse
from ast import unparse as pyast_unparse
from typing import List, Optional, Union, cast

from redbaron import RedBaron

from automata.singletons.py_module_loader import py_module_loader, pyast_module_loader
from automata.symbol.base import Symbol, SymbolDescriptor

AstNode = Union[AsyncFunctionDef, ClassDef, FunctionDef, Module]


def get_descriptor_kind_from_node(node) -> Optional[SymbolDescriptor.PyKind]:
    if isinstance(node, FunctionDef) or isinstance(node, AsyncFunctionDef):
        return SymbolDescriptor.PyKind.Method
    elif isinstance(node, ClassDef):
        return SymbolDescriptor.PyKind.Class
    elif isinstance(node, Module):
        return SymbolDescriptor.PyKind.Module
    else:
        return None


def is_node_matching_descriptor(node: AstNode, descriptor: SymbolDescriptor):
    descriptor_kind = SymbolDescriptor.convert_scip_to_python_suffix(descriptor.suffix)
    node_descriptor = get_descriptor_kind_from_node(node)
    if node_descriptor == descriptor_kind:
        if isinstance(node, Module):
            return True
        return node.name == descriptor.name


def visit(node: AstNode, descriptors: List[SymbolDescriptor], level=0) -> Optional[AST]:
    if level >= len(descriptors):
        return None

    if not is_node_matching_descriptor(node, descriptors[level]):
        return None

    if level == len(descriptors) - 1:
        return node

    for child in iter_child_nodes(node):
        if not isinstance(child, (ClassDef, FunctionDef, AsyncFunctionDef)):
            continue
        result = visit(child, descriptors, level + 1)
        if result:
            return result

    return None


def get_source_code_of_symbol_using_py_ast(symbol: Symbol) -> AST:
    descriptors = list(symbol.descriptors)
    module_dotpath = descriptors[0].name
    if module_dotpath.startswith(""):
        module_dotpath = module_dotpath[len("") :]  # indexer omits this
    tree = pyast_module_loader.fetch_module(module_dotpath)
    if not tree or not isinstance(tree, Module):
        raise ValueError(
            f"Either the module {module_dotpath} was not found or it is not an Python's module object"
        )
    node = visit(tree, descriptors)
    if node is None:
        raise ValueError(f"Failed to find {symbol.uri} in source code")
    return node


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
            obj = cast(RedBaron, py_module_loader.fetch_module(module_dotpath))
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
