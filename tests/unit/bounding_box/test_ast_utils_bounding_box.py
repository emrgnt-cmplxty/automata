import ast
from ast import parse
from typing import cast

import pytest

from automata.code_parsers.py.ast_utils import (
    BoundingBox,
    LineItem,
    fetch_bounding_box,
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


def test_fetch_bounding_box_with_function_node():
    node = parse("def foo():\n    pass\n")
    function_node = node.body[0]
    bounding_box = fetch_bounding_box(function_node)
    assert bounding_box.top_left.line == 1
    assert bounding_box.top_left.column == 0
    assert bounding_box.bottom_right.line == 2
    assert bounding_box.bottom_right.column == 8


def test_fetch_bounding_box_with_incomplete_node():
    node = parse("foo")
    node.end_lineno = None
    bounding_box = fetch_bounding_box(node)
    assert bounding_box is None


def test_fetch_bounding_box_with_class_node():
    node = parse("class Foo:\n    pass\n")
    class_node = node.body[0]
    bounding_box = fetch_bounding_box(class_node)
    assert bounding_box.top_left.line == 1
    assert bounding_box.top_left.column == 0
    assert bounding_box.bottom_right.line == 2
    assert bounding_box.bottom_right.column == 8


def test_fetch_bounding_box_with_class_node_in_file():
    with open("tests/unit/sample_modules/sample3.py") as f:
        file_content = f.read()

    module = ast.parse(file_content)

    class_node = module.body[0]
    bounding_box = fetch_bounding_box(class_node)

    assert bounding_box.top_left.line == 1
    assert bounding_box.top_left.column == 0
    assert bounding_box.bottom_right.line == 6
    assert bounding_box.bottom_right.column == 12


def test_fetch_bounding_box_with_method_node():
    with open("tests/unit/sample_modules/sample3.py") as f:
        file_content = f.read()

    module = ast.parse(file_content)

    class_node = module.body[0]
    method_node = class_node.body[1]
    bounding_box = fetch_bounding_box(method_node)

    assert bounding_box.top_left.line == 4
    assert bounding_box.top_left.column == 4
    assert bounding_box.bottom_right.line == 6
    assert bounding_box.bottom_right.column == 12


def test_fetch_bounding_box_with_function_node_in_file():
    with open("tests/unit/sample_modules/sample3.py") as f:
        file_content = f.read()

    module = ast.parse(file_content)

    function_node = module.body[1]
    bounding_box = fetch_bounding_box(function_node)

    assert bounding_box.top_left.line == 9
    assert bounding_box.top_left.column == 0
    assert bounding_box.bottom_right.line == 11
    assert bounding_box.bottom_right.column == 8
