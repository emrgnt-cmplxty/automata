import ast
import inspect
import os

import pytest

from automata.code_parsers.py import ContextComponent, PyContextRetriever
from automata.core.utils import get_root_fpath
from automata.singletons.py_module_loader import py_module_loader
from automata.symbol import parse_symbol

from .sample_modules.my_project.core.calculator import Calculator


# TODO - Unify module loader fixture
@pytest.fixture(autouse=True)
def local_module_loader():
    # FIXME - This can't be a good pattern, let's cleanup later.
    py_module_loader.reset()
    py_module_loader.initialize(
        os.path.join(get_root_fpath(), "tests", "unit", "sample_modules"), "my_project"
    )
    yield py_module_loader


@pytest.fixture
def context_retriever():
    return PyContextRetriever()


def test_process_symbol(context_retriever):
    symbol = parse_symbol(
        "scip-python python automata v0.0.0 `my_project.core.calculator`/Calculator#"
    )
    components = {
        ContextComponent.HEADLINE: {},
        ContextComponent.INTERFACE: {"skip_private": True},
    }
    context = context_retriever.process_symbol(symbol, components)
    assert "Building context for symbol -" in context
    assert "add(self, a: int, b: int) -> int" in context


def test_process_symbol_error(context_retriever):
    symbol = parse_symbol(
        "scip-python python automata v0.0.0 `my_project.core.calculator`/Calculator#"
    )
    components = {ContextComponent.SOURCE_CODE: {}, ContextComponent.INTERFACE: {}}
    with pytest.raises(ValueError):
        context_retriever.process_symbol(symbol, components)


def test_process_symbol_invalid_component(context_retriever, caplog):
    symbol = parse_symbol(
        "scip-python python automata v0.0.0 `my_project.core.calculator`/Calculator#"
    )
    components = {ContextComponent.HEADLINE: {}, "invalid_component": {}}
    context_retriever.process_symbol(symbol, components)
    assert "Warning: invalid_component is not a valid context component." in caplog.text


def test_source_code(context_retriever):
    symbol = parse_symbol(
        "scip-python python automata v0.0.0 `my_project.core.calculator`/Calculator#"
    )
    ast_object = ast.parse(inspect.getsource(Calculator))
    source_code = context_retriever._source_code(
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
    source_code = context_retriever._source_code(
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
    interface = context_retriever._interface(symbol, ast_object, skip_private=True)
    print("interface = ", interface)
    print("-" * 100)
    assert "Interface:" in interface
    assert "add(self, a: int, b: int) -> int" in interface


def test_interface_recursion_error(context_retriever):
    symbol = parse_symbol(
        "scip-python python automata v0.0.0 `my_project.core.calculator`/Calculator#"
    )
    ast_object = ast.parse(inspect.getsource(Calculator))
    with pytest.raises(RecursionError):
        context_retriever._interface(symbol, ast_object, recursion_depth=3)


def test_process_headline(context_retriever):
    symbol = parse_symbol(
        "scip-python python automata v0.0.0 `my_project.core.calculator`/Calculator#"
    )
    ast_object = ast.parse(inspect.getsource(Calculator))
    headline = context_retriever._process_headline(symbol, ast_object)
    assert headline == "Building context for symbol - my_project.core.calculator.Calculator\n"


def test_process_method(context_retriever):
    source_code = inspect.getsource(Calculator.add)
    # Remove the leading spaces from the source code
    source_code = "\n".join(
        [
            line[len("    ") :] if line.startswith("    ") else line
            for line in source_code.split("\n")
        ]
    )
    ast_object = ast.parse(source_code).body[0]
    processed_method = context_retriever._process_method(ast_object)
    assert processed_method == "add(self, a: int, b: int) -> int\n"


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
    return_annotation = context_retriever._get_method_return_annotation(ast_object)
    assert return_annotation == "int"


def test_is_private_method(context_retriever):
    source_code = "def _private_method(): pass"
    ast_object = ast.parse(source_code).body[0]
    assert context_retriever._is_private_method(ast_object)


def test_get_all_methods(context_retriever):
    source_code = inspect.getsource(Calculator)
    ast_object = ast.parse(source_code)
    methods = context_retriever._get_all_methods(ast_object)
    assert len(methods) == 3
    assert all(isinstance(method, (ast.FunctionDef, ast.AsyncFunctionDef)) for method in methods)


def test_get_all_classes(context_retriever):
    import textwrap

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
    classes = context_retriever._get_all_classes(ast_object)
    assert len(classes) == 2
    assert all(isinstance(cls, ast.ClassDef) for cls in classes)


def test_interface_include_docstrings(context_retriever):
    symbol = parse_symbol(
        "scip-python python automata v0.0.0 `my_project.core.calculator`/Calculator#"
    )
    ast_object = ast.parse(inspect.getsource(Calculator))
    interface = context_retriever._interface(symbol, ast_object, include_docstrings=True)
    assert "Interface:" in interface
    assert "add(self, a: int, b: int) -> int" in interface
    assert "Docstring for Calculator class" in interface
    assert "Docstring for add method" in interface


def test_interface_exclude_docstrings(context_retriever):
    symbol = parse_symbol(
        "scip-python python automata v0.0.0 `my_project.core.calculator`/Calculator#"
    )
    ast_object = ast.parse(inspect.getsource(Calculator))
    interface = context_retriever._interface(symbol, ast_object, include_docstrings=False)
    assert "Interface:" in interface
    assert "add(self, a: int, b: int) -> int" in interface
    assert "Docstring for Calculator class" not in interface
    assert "Docstring for add method" not in interface
