import ast
import pytest
from ast import parse
from typing import cast
from automata.code_parsers.py.ast_utils import (
    LineItem,
    BoundingBox,
    fetch_bounding_box,
    get_docstring_from_node,
    get_node_without_docstrings,
    get_node_without_imports,
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


def test_fetch_bounding_box_with_class_node():
    node = parse("class Foo:\n    pass\n")
    class_node = node.body[0]
    bounding_box = fetch_bounding_box(class_node)
    assert bounding_box.top_left.line == 1
    assert bounding_box.top_left.column == 0
    assert bounding_box.bottom_right.line == 2
    assert bounding_box.bottom_right.column == 8


def test_get_node_without_docstrings():
    node = parse("def foo():\n" '    """This is a docstring."""\n' "    pass\n")
    node_without_docstrings = get_node_without_docstrings(node.body[0])
    assert get_docstring_from_node(node_without_docstrings) == "No result found."


def test_get_node_without_imports():
    node = parse("import os\ndef foo():\n" '    """This is a docstring."""\n' "    pass\n")
    module_node = cast(ast.Module, node)
    node_without_imports = get_node_without_imports(module_node)
    assert isinstance(node_without_imports.body[0], ast.FunctionDef)  # skip the import statement


@pytest.mark.parametrize(
    "source,expected",
    [
        ('def foo():\n    """This is a docstring."""\n    pass\n', "This is a docstring."),
        (
            'class Foo:\n    """This is a class docstring."""\n    pass\n',
            "This is a class docstring.",
        ),
        ("foo = 10", "No result found."),
        ("import os", "No result found."),
        ("from os import path", "No result found."),
        ("# this is a comment", "No result found."),
        (
            '"""This is a standalone docstring."""\n"""Another standalone string."""',
            "This is a standalone docstring.",
        ),
    ],
)
def test_get_docstring_from_node_with_various_nodes(source, expected):
    module = parse(source)
    if module.body and isinstance(
        module.body[0], (ast.AsyncFunctionDef, ast.ClassDef, ast.FunctionDef, ast.Module)
    ):
        node = module.body[0]
    else:
        node = module
    docstring = get_docstring_from_node(node)
    assert docstring == expected


@pytest.mark.parametrize(
    "source",
    [
        'def foo():\n    """This is a docstring."""\n    pass\n',
        'class Foo:\n    """This is a class docstring."""\n    pass\n',
        "foo = 10",
        '"""This is a standalone docstring."""',
    ],
)
def test_get_node_without_docstrings_with_various_nodes(source):
    node = parse(source)
    node_without_docstrings = get_node_without_docstrings(node)
    assert get_docstring_from_node(node_without_docstrings) == "No result found."


@pytest.mark.parametrize(
    "source",
    [
        "import os\ndef foo():\n    pass\n",
        "from os import path\ndef foo():\n    pass\n",
        "def foo():\n    pass\n",
    ],
)
def test_get_node_without_imports_with_various_nodes(source):
    node = parse(source)
    node_without_imports = get_node_without_imports(node)
    if "import" in source:
        assert not isinstance(node_without_imports.body[0], (ast.Import, ast.ImportFrom))
    else:
        assert isinstance(node_without_imports.body[0], ast.FunctionDef)


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
