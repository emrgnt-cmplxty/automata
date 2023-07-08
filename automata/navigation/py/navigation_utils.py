from __future__ import annotations

import logging
from ast import AST, AsyncFunctionDef, ClassDef, FunctionDef
from ast import Module as ModuleNode
from ast import iter_child_nodes
from dataclasses import dataclass
from typing import List, Union

logger = logging.getLogger(__name__)


def find_syntax_tree_node_pyast(code_obj: Union[ModuleNode, AST], object_path: List[str]):
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
