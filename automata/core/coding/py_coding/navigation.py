from __future__ import annotations

import logging
from typing import Optional, Union

from automata_docs.core.coding.py_coding.py_utils import DOT_SEP
from redbaron import (
    ClassNode,
    DefNode,
    FromImportNode,
    ImportNode,
    Node,
    NodeList,
    RedBaron,
)

logger = logging.getLogger(__name__)


def find_syntax_tree_node(
    code_obj: Optional[Union[RedBaron, ClassNode]], object_path: Optional[str]
) -> Optional[Union[Node, RedBaron]]:
    """
    Find a module, or find a function, method, or class inside a module.

    Args:
        code_obj (RedBaron): The  red baron FST object.
        object_path (Optional[str]): The dot-separated object path (e.g., 'ClassName.method_name'). If None,
            the module is returned.

    Returns:
        Optional[Union[Def, Class, Module]]: The found def, or class node, or None if not found.
    """
    if not code_obj:
        return None

    if not object_path:
        return code_obj

    obj_parts = object_path.split(DOT_SEP)

    node = code_obj
    while node and obj_parts:
        obj_name = obj_parts.pop(0)
        node = _find_subnode(node, obj_name)
    return node


def find_import_syntax_tree_nodes(module: RedBaron) -> Optional[NodeList]:
    """
    Find all imports in a module.

    Args:
        module (RedBaron): The module to search.

    Returns:
        Optional[NodeList]: A list of ImportNode and FromImportNode objects.
    """
    return module.find_all(lambda identifier: identifier in ("import", "from_import"))


def find_import_syntax_tree_node_by_name(
    module: RedBaron, import_name: str
) -> Optional[Union[ImportNode, FromImportNode]]:
    """
    Find an import by name.

    Args:
        module (RedBaron): The module to search.
        import_name (str): The name of the import to find.

    Returns:
        Optional[Union[ImportNode, FromImportNode]]: The found import, or None if not found.
    """
    return module.find(
        lambda identifier: identifier in ("import", "from_import"), name=import_name
    )


def find_all_function_and_class_syntax_tree_nodes(module: RedBaron) -> NodeList:
    """
    Find all imports in a module.

    Args:
        module (RedBaron): The module to search.

    Returns:
        NodeList: A list of ClassNode and DefNode objects.
    """
    return module.find_all(lambda identifier: identifier in ("class", "def"))


def find_method_call_by_location(
    module: RedBaron, line_number: int, column_number: int
) -> Optional[RedBaron]:
    """
    Find a method call by a symbol reference in a module.

    Args:
        module (RedBaron): The module to search.
        line_number (int): The line number of the symbol reference.
        column_number (int): The column number of the symbol reference.

    Returns:
        Optional[Node]: The found node, or None if not found.
    """
    try:
        # Find all CallNode instances
        all_calls = module.find_all("call")
        for call in all_calls:
            # Check if call start is before and end is after our reference point
            if (
                call.absolute_bounding_box.top_left.line - 1 < line_number
                or (
                    call.absolute_bounding_box.top_left.line - 1 == line_number
                    and call.absolute_bounding_box.top_left.column - 1 <= column_number
                )
            ) and (
                call.absolute_bounding_box.bottom_right.line - 1 > line_number
                or (
                    call.absolute_bounding_box.bottom_right.line - 1 == line_number
                    and call.absolute_bounding_box.bottom_right.column - 1 >= column_number
                )
            ):
                return call
        return None
    except IndexError:
        return None


def _find_subnode(code_obj: RedBaron, obj_name: str) -> Optional[Union[DefNode, ClassNode]]:
    """
    Find a DefNode or ClassNode node with the specified name within the given
    FST code object.

    Args:
        code_obj (RedBaron): The FST code object (RedBaron or Node) to search.
        obj_name (str): The name of the object to find.

    Returns:
        Optional[Union[DefNode, ClassNode]]: The found node, or None.
    """
    return code_obj.find(lambda identifier: identifier in ("def", "class"), name=obj_name)
