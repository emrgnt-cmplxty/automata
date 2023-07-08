from __future__ import annotations

import logging
from ast import AST, AsyncFunctionDef, ClassDef, FunctionDef
from ast import Module
from ast import Module as ModuleNode
from ast import iter_child_nodes
from dataclasses import dataclass
from typing import List, Optional, Union

from automata.core.base.ast import ASTNode
from automata.symbol.base import SymbolDescriptor

logger = logging.getLogger(__name__)


def find_syntax_tree_node_py_ast(code_obj: Union[ModuleNode, AST], object_path: List[str]):
    def find_subnode(node, obj_name):
        for child in iter_child_nodes(node):
            if (
                isinstance(child, (ClassDef, FunctionDef, AsyncFunctionDef))
                and child.name == obj_name
            ):
                return child
        return None

    if isinstance(code_obj, (ModuleNode, ClassDef)):
        node = code_obj
        while node and object_path:
            obj_name = object_path.pop(0)
            node = find_subnode(node, obj_name)
        return node
    return None


@dataclass
class LineItem:
    """A class to represent a line item in a bounding box."""

    line: int
    column: int


@dataclass
class BoundingBox:
    """A class to represent the bounding box of a symbol."""

    top_left: LineItem
    bottom_right: LineItem


def construct_bounding_box(node: AST) -> BoundingBox:
    if not node.end_lineno:
        raise ValueError(f"{node} does not have an end line number")
    elif not node.end_col_offset:
        raise ValueError(f"{node} does not have an end column offset")

    return BoundingBox(
        top_left=LineItem(line=node.lineno, column=node.col_offset),
        bottom_right=LineItem(line=node.end_lineno, column=node.end_col_offset),
    )


def get_descriptor_kind_from_node(node) -> Optional[SymbolDescriptor.PyKind]:
    if isinstance(node, FunctionDef) or isinstance(node, AsyncFunctionDef):
        return SymbolDescriptor.PyKind.Method
    elif isinstance(node, ClassDef):
        return SymbolDescriptor.PyKind.Class
    elif isinstance(node, Module):
        return SymbolDescriptor.PyKind.Module
    else:
        return None


def is_node_matching_descriptor(node: ASTNode, descriptor: SymbolDescriptor):
    descriptor_kind = SymbolDescriptor.convert_scip_to_python_suffix(descriptor.suffix)
    node_descriptor = get_descriptor_kind_from_node(node)
    if node_descriptor == descriptor_kind:
        if isinstance(node, Module):
            return True
        return node.name == descriptor.name


def visit(node: ASTNode, descriptors: List[SymbolDescriptor], level=0) -> Optional[AST]:
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
