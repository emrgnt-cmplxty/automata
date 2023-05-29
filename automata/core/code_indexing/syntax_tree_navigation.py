from __future__ import annotations

import logging
from typing import Optional, Union

from redbaron import ClassNode, DefNode, FromImportNode, ImportNode, Node, NodeList, RedBaron

from automata.core.code_indexing.utils import DOT_SEP

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
