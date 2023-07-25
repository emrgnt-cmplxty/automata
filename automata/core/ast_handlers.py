from __future__ import annotations

import logging
from ast import (
    AST,
    AsyncFunctionDef,
    ClassDef,
    Expr,
    FunctionDef,
    Import,
    ImportFrom,
    Module,
    NodeTransformer,
    Str,
    get_docstring,
    iter_child_nodes,
)
from dataclasses import dataclass
from typing import List, Optional

logger = logging.getLogger(__name__)

AST_NO_RESULT_FOUND = "No result found."


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


def fetch_bounding_box(node: AST) -> Optional[BoundingBox]:
    """Finds the bounding box of a node in the AST."""

    if not node.end_lineno or not node.end_col_offset:
        logger.warning(
            f"{node} does not have an end line number or column offset"
        )
        return None
    return BoundingBox(
        top_left=LineItem(line=node.lineno, column=node.col_offset),
        bottom_right=LineItem(
            line=node.end_lineno, column=node.end_col_offset
        ),
    )


def get_docstring_from_node(node: Optional[AST]) -> str:
    """Gets the docstring from the specified node."""

    if not node:
        return AST_NO_RESULT_FOUND

    elif isinstance(node, (AsyncFunctionDef, ClassDef, FunctionDef, Module)):
        if doc_string := get_docstring(node):
            return doc_string.replace('"""', "").replace("'''", "")
        else:
            return AST_NO_RESULT_FOUND
    return ""


class DocstringRemover(NodeTransformer):
    """Removes docstrings from a class or function."""

    def visit(self, node):
        # If this node is a function, class, or module, remove its docstring.
        if (
            isinstance(node, (AsyncFunctionDef, ClassDef, FunctionDef, Module))
            and isinstance(node.body[0], Expr)
            and isinstance(node.body[0].value, Str)
        ):
            node.body.pop(0)
        return super().visit(node)


def get_node_without_docstrings(node: AST) -> AST:
    """Creates a copy of the specified node without docstrings."""

    remover = DocstringRemover()
    remover.visit(node)
    return node


class ImportRemover(NodeTransformer):
    """Removes import statements from a module, class or function."""

    def visit(self, node):
        # If this node is a function, class, or module, and its first child is an import statement,
        # remove the import statement.
        if isinstance(
            node, (AsyncFunctionDef, ClassDef, FunctionDef, Module)
        ) and (isinstance(node.body[0], (Import, ImportFrom))):
            node.body.pop(0)
        return super().visit(node)


def get_node_without_imports(node: AST) -> AST:
    """Creates a copy of the specified node without import statements."""

    remover = ImportRemover()
    remover.visit(node)
    return node


def find_imports(module: Module) -> List[AST]:
    """Find the imports for a specified module."""

    return [
        node for node in module.body if isinstance(node, (Import, ImportFrom))
    ]


def find_syntax_tree_node(
    code_obj: Optional[AST],
    node_path: Optional[str],
) -> Optional[AST]:
    """Find a module, or find a function, method, or class inside a module."""

    if not code_obj:
        return None

    if not node_path:
        return code_obj

    obj_parts = node_path.split(".")

    def find_syntax_tree_node_pyast(code_obj: AST, node_path: List[str]):
        """Finds the syntax tree node using the pyast library."""

        def find_subnode(node, obj_name):
            """Finds a subnode of a node with the specified name."""

            for child in iter_child_nodes(node):
                if (
                    isinstance(
                        child,
                        (Module, ClassDef, FunctionDef, AsyncFunctionDef),
                    )
                    and child.name == obj_name
                ):
                    return child
            return None

        if isinstance(code_obj, (Module, ClassDef)):
            """Check if the code object is a module or class."""

            node = code_obj
            while node and node_path:
                obj_name = node_path.pop(0)
                node = find_subnode(node, obj_name)
            return node
        return None

    return find_syntax_tree_node_pyast(code_obj, obj_parts)
