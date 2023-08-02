import ast
import inspect
import os
import textwrap

import pytest

from automata.core.utils import get_root_py_fpath
from automata.experimental.code_parsers import (
    ContextComponent,
    PyContextRetriever,
)
from automata.experimental.code_parsers.py.context_processing.context_utils import (
    _get_method_return_annotation,
    get_all_classes,
    get_all_methods,
    is_private_method,
    process_method,
)
from automata.singletons.py_module_loader import py_module_loader
from automata.symbol import parse_symbol
from automata.tests.unit.sample_modules.my_project.core.calculator import (
    Calculator,
)


# TODO - Unify module loader fixture
@pytest.fixture(autouse=True)
def local_module_loader():
    # FIXME - This can't be a good pattern, let's cleanup later.
    py_module_loader.reset()
    py_module_loader.initialize(
        os.path.join(get_root_py_fpath(), "tests", "unit", "sample_modules"),
        "my_project",
    )
    yield py_module_loader


@pytest.fixture
def context_retriever():
    return PyContextRetriever()


def test_process_symbol_interface(context_retriever):
    symbol = parse_symbol(
        "scip-python python automata v0.0.0 `my_project.core.calculator`/Calculator#"
    )
    components = {
        ContextComponent.HEADLINE: {},
        ContextComponent.INTERFACE: {"skip_private": True},
    }
    context = context_retriever.process_symbol(symbol, components)
    assert "my_project.core.calculator.Calculator" in context
    assert "Interface" in context
    assert "add(self, a: int, b: int) -> int" in context


def test_process_symbol_source(context_retriever):
    symbol = parse_symbol(
        "scip-python python automata v0.0.0 `my_project.core.calculator`/Calculator#"
    )
    components = {
        ContextComponent.HEADLINE: {},
        ContextComponent.SOURCE_CODE: {"skip_private": True},
    }
    context = context_retriever.process_symbol(symbol, components)
    assert "my_project.core.calculator.Calculator" in context
    assert "Interface" not in context
    assert "add(self, a: int, b: int) -> int" in context
    assert "return a + b" in context


def test_process_symbol_error(context_retriever):
    symbol = parse_symbol(
        "scip-python python automata v0.0.0 `my_project.core.calculator`/Calculator#"
    )
    components = {
        ContextComponent.SOURCE_CODE: {},
        ContextComponent.INTERFACE: {},
    }
    with pytest.raises(ValueError):
        context_retriever.process_symbol(symbol, components)


def test_process_symbol_invalid_component(context_retriever, caplog):
    symbol = parse_symbol(
        "scip-python python automata v0.0.0 `my_project.core.calculator`/Calculator#"
    )
    components = {ContextComponent.HEADLINE: {}, "invalid_component": {}}
    context_retriever.process_symbol(symbol, components)
    assert (
        "Warning: invalid_component is not a valid context component."
        in caplog.text
    )


def test_source_code(context_retriever):
    symbol = parse_symbol(
        "scip-python python automata v0.0.0 `my_project.core.calculator`/Calculator#"
    )
    ast_object = ast.parse(inspect.getsource(Calculator))
    source_code = context_retriever.context_components[
        ContextComponent.SOURCE_CODE
    ].generate(
        symbol, ast_object, include_imports=False, include_docstrings=True
    )
    assert "class Calculator:" in source_code
    assert "def add(self, a: int, b: int) -> int:" in source_code
    assert "return a + b" in source_code


def test_source_code_2(context_retriever):
    symbol = parse_symbol(
        "scip-python python automata v0.0.0 `my_project.core.calculator`/Calculator#"
    )
    ast_object = ast.parse(inspect.getsource(Calculator))
    source_code = context_retriever.context_components[
        ContextComponent.SOURCE_CODE
    ].generate(
        symbol, ast_object, include_imports=True, include_docstrings=True
    )
    assert "import math" in source_code
    assert "class Calculator:" in source_code
    assert "def add(self, a: int, b: int) -> int:" in source_code
    assert "return a + b" in source_code


def test_interface(context_retriever):
    symbol = parse_symbol(
        "scip-python python automata v0.0.0 `my_project.core.calculator`/Calculator#"
    )
    ast_object = ast.parse(inspect.getsource(Calculator))
    interface = context_retriever.context_components[
        ContextComponent.INTERFACE
    ].generate(symbol, ast_object, skip_private=True)
    assert "Interface:" in interface
    assert "add(self, a: int, b: int) -> int" in interface


def test_interface_recursion_error(context_retriever):
    symbol = parse_symbol(
        "scip-python python automata v0.0.0 `my_project.core.calculator`/Calculator#"
    )
    ast_object = ast.parse(inspect.getsource(Calculator))
    with pytest.raises(RecursionError):
        context_retriever.context_components[
            ContextComponent.INTERFACE
        ].generate(symbol, ast_object, recursion_depth=3)


def test_process_headline(context_retriever):
    symbol = parse_symbol(
        "scip-python python automata v0.0.0 `my_project.core.calculator`/Calculator#"
    )
    ast_object = ast.parse(inspect.getsource(Calculator))
    headline = context_retriever.context_components[
        ContextComponent.HEADLINE
    ].generate(symbol, ast_object)
    assert headline == "my_project.core.calculator.Calculator\n"


def testprocess_method(context_retriever):
    source_code = inspect.getsource(Calculator.add)
    # Remove the leading spaces from the source code
    source_code = "\n".join(
        [
            line[len("    ") :] if line.startswith("    ") else line
            for line in source_code.split("\n")
        ]
    )
    ast_object = ast.parse(source_code).body[0]
    processed_method = process_method(ast_object)
    assert processed_method == "add(self, a: int, b: int) -> int"


def test_get_method_return_annotation(context_retriever):
    source_code = inspect.getsource(Calculator.add)
    # Remove the leading spaces from the source code
    source_code = "\n".join(
        [
            line[len("    ") :] if line.startswith("    ") else line
            for line in source_code.split("\n")
        ]
    )
    ast_object = ast.parse(source_code).body[0]
    return_annotation = _get_method_return_annotation(ast_object)
    assert return_annotation == "int"


def testis_private_method(context_retriever):
    source_code = "def _private_method(): pass"
    ast_object = ast.parse(source_code).body[0]
    assert is_private_method(ast_object)


def test_dunder_is_not_private(context_retriever):
    source_code = "def __init__(self): pass"
    ast_object = ast.parse(source_code).body[0]
    assert not is_private_method(ast_object)


def testget_all_methods(context_retriever):
    source_code = inspect.getsource(Calculator)
    ast_object = ast.parse(source_code)
    methods = get_all_methods(ast_object)
    assert len(methods) == 3
    assert all(
        isinstance(method, (ast.FunctionDef, ast.AsyncFunctionDef))
        for method in methods
    )


def testget_all_classes(context_retriever):
    source = textwrap.dedent(
        """
    class Calculator:
        def add(self, a, b):
            return a + b

        def subtract(self, a, b):
            return a - b

        class Calculator4:
            pass
    """
    )
    ast_object = ast.parse(source)
    classes = get_all_classes(ast_object)
    assert len(classes) == 2
    assert all(isinstance(cls, ast.ClassDef) for cls in classes)


def test_interface_include_docstrings(context_retriever):
    symbol = parse_symbol(
        "scip-python python automata v0.0.0 `my_project.core.calculator`/Calculator#"
    )
    ast_object = ast.parse(inspect.getsource(Calculator))
    interface = context_retriever.context_components[
        ContextComponent.INTERFACE
    ].generate(symbol, ast_object, include_docstrings=True)
    assert "Interface:" in interface
    assert "add(self, a: int, b: int) -> int" in interface
    assert "Docstring for Calculator class" in interface
    assert "Docstring for add method" in interface


def test_interface_exclude_docstrings(context_retriever):
    symbol = parse_symbol(
        "scip-python python automata v0.0.0 `my_project.core.calculator`/Calculator#"
    )
    ast_object = ast.parse(inspect.getsource(Calculator))
    interface = context_retriever.context_components[
        ContextComponent.INTERFACE
    ].generate(symbol, ast_object, include_docstrings=False)
    assert "Interface:" in interface
    assert "add(self, a: int, b: int) -> int" in interface
    assert "Docstring for Calculator class" not in interface
    assert "Docstring for add method" not in interface


def test_class_inheritance(context_retriever):
    class Parent:
        pass

    class Child(Parent):
        pass

    source_code = inspect.getsource(Child)
    source_code = textwrap.dedent(source_code)
    ast_object = ast.parse(source_code)
    class_details = context_retriever.context_components[
        ContextComponent.INTERFACE
    ].generate(None, ast_object)
    assert "Parent" in class_details


def test_dunder_not_private(context_retriever):
    class MyClass:
        def __init__(self):
            pass

    source_code = inspect.getsource(MyClass.__init__)
    source_code = textwrap.dedent(source_code)

    ast_object = ast.parse(source_code).body[0]
    assert not is_private_method(ast_object)


def test_nested_class_detection(context_retriever):
    class Parent:
        class Child:
            pass

    source_code = inspect.getsource(Parent)
    source_code = textwrap.dedent(source_code)

    ast_object = ast.parse(source_code)
    classes = get_all_classes(ast_object)
    assert len(classes) == 2
    assert all(isinstance(cls, ast.ClassDef) for cls in classes)
    assert any(cls.name == "Child" for cls in classes)


def test_class_inheritance_in_source_code(context_retriever):
    class Parent:
        pass

    class Child(Parent):
        pass

    source_code = inspect.getsource(Child)
    source_code = textwrap.dedent(source_code)
    ast_object = ast.parse(source_code)
    result_code = context_retriever.context_components[
        ContextComponent.INTERFACE
    ].generate(
        None, ast_object, include_imports=False, include_docstrings=True
    )
    assert "class Child(Parent):" in result_code


def test_class_attributes_in_source_code(context_retriever):
    class TestClass:
        attr1: int
        attr2: str

    source_code = inspect.getsource(TestClass)
    source_code = textwrap.dedent(source_code)
    ast_object = ast.parse(source_code)
    result_code = context_retriever.context_components[
        ContextComponent.INTERFACE
    ].generate(
        None, ast_object, include_imports=False, include_docstrings=True
    )
    assert "attr1: int" in result_code
    assert "attr2: str" in result_code


@pytest.mark.skip("TODO - Fix this test")
def test_constructor_and_attributes(context_retriever):
    class MyClass:
        def __init__(self, attr1: int, attr2: str):
            """These are some docstrings"""
            self.attr1 = attr1
            self.attr2 = attr2
            self.attr3: float = 0.3

        def another_test(self):
            pass

        def another_another_test(self, x: int, y: float = 0.1):
            pass

    source_code = inspect.getsource(MyClass)
    source_code = textwrap.dedent(source_code)
    ast_object = ast.parse(source_code)
    result_code = context_retriever.context_components[
        ContextComponent.INTERFACE
    ].generate(
        None, ast_object, include_imports=False, include_docstrings=True
    )
    assert "attr1: int" in result_code
    assert "attr2: str" in result_code
    assert (
        "attr3: float" in result_code
    )  # this is where the current test will fail!
    assert "init" in result_code
