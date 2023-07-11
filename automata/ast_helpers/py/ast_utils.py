from __future__ import annotations

import logging
from ast import (
    AST,
    AsyncFunctionDef,
    ClassDef,
    Expr,
    FunctionDef,
    Module,
    NodeTransformer,
    Str,
    get_docstring,
)
from dataclasses import dataclass
from typing import Optional, Union

logger = logging.getLogger(__name__)


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


def get_docstring_from_node(node: Optional[AST]) -> str:
    """
    Gets the docstring from the specified node
    Args:
        node: The AST node to get the docstring from
    """
    if not node:
        return "No result found."

    elif isinstance(node, (FunctionDef, ClassDef, AsyncFunctionDef)):
        doc_string = get_docstring(node)
        if doc_string:
            doc_string.replace('"""', "").replace("'''", "")
            return doc_string
        else:
            return "No result found."
    return ""


class DocstringRemover(NodeTransformer):
    """Removes docstrings from a class or function."""

    def visit(self, node):
        # If this node is a function, class, or module, remove its docstring.
        if isinstance(node, (FunctionDef, AsyncFunctionDef, ClassDef, Module)):
            if isinstance(node.body[0], Expr) and isinstance(node.body[0].value, Str):
                node.body.pop(0)
        return super().visit(node)


def remove_docstrings(tree: Union[FunctionDef, AsyncFunctionDef, ClassDef, Module]):
    remover = DocstringRemover()
    remover.visit(tree)
    return tree
