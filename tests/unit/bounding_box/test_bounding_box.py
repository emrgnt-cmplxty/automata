import pytest
from ast import parse
from automata.code_parsers.py.ast_utils import (
    LineItem,
    BoundingBox,
    construct_bounding_box,
    get_docstring_from_node,
)


@pytest.fixture
def line_item():
    return LineItem(10, 20)


@pytest.fixture
def bounding_box(line_item):
    return BoundingBox(top_left=line_item, bottom_right=line_item)


def test_line_item_creation(line_item):
    assert line_item.line == 10
    assert line_item.column == 20


def test_bounding_box_creation(bounding_box, line_item):
    assert bounding_box.top_left == line_item
    assert bounding_box.bottom_right == line_item


def test_construct_bounding_box_with_function_node():
    node = parse("def foo():\n    pass\n")
    function_node = node.body[0]
    bounding_box = construct_bounding_box(function_node)
    assert bounding_box.top_left.line == 1
    assert bounding_box.top_left.column == 0
    assert bounding_box.bottom_right.line == 2
    assert bounding_box.bottom_right.column == 8


def test_construct_bounding_box_with_incomplete_node():
    node = parse("foo")
    node.end_lineno = None
    bounding_box = construct_bounding_box(node)
    assert bounding_box is None


def test_get_docstring_from_node_with_docstring():
    node = parse("def foo():\n" '    """This is a docstring."""\n' "    pass\n")
    docstring = get_docstring_from_node(node.body[0])
    assert docstring == "This is a docstring."


def test_get_docstring_from_node_without_docstring():
    node = parse("def foo():\n" "    pass\n")
    docstring = get_docstring_from_node(node)
    assert docstring == "No result found."


def test_get_docstring_from_node_with_none_node():
    docstring = get_docstring_from_node(None)
    assert docstring == "No result found."
