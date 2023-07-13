import ast
import os

import pytest

from automata.core.utils import get_root_fpath
from automata.singletons.py_module_loader import py_module_loader
from automata.symbol import convert_to_ast_object, get_rankable_symbols, parse_symbol


# TODO - Unify module loader fixture
@pytest.fixture(autouse=True)
def local_module_loader():
    # FIXME - This can't be a good pattern, let's cleanup later.
    py_module_loader.reset()

    py_module_loader.initialize(
        os.path.join(get_root_fpath(), "tests", "unit", "sample_modules"), "my_project"
    )
    yield py_module_loader


def test_convert_to_ast_object(local_module_loader):
    # Create a symbol representing a class
    class_symbol = parse_symbol(
        "scip-python python automata v0.0.0 `my_project.core.calculator`/Calculator#"
    )
    ast_obj = convert_to_ast_object(class_symbol)
    assert isinstance(ast_obj, ast.ClassDef)

    # Create a symbol representing a method
    method_symbol = parse_symbol(
        "scip-python python automata v0.0.0 `my_project.core.calculator`/Calculator#__init__()."
    )
    ast_obj = convert_to_ast_object(method_symbol)
    assert isinstance(ast_obj, (ast.FunctionDef, ast.AsyncFunctionDef))

    nested_class_symbol = parse_symbol(
        "scip-python python automata v0.0.0 `my_project.core.extended.calculator3`/Calculator3#Calculator4#"
    )
    ast_obj = convert_to_ast_object(nested_class_symbol)
    assert isinstance(ast_obj, ast.ClassDef)


def test_get_rankable_symbols(local_module_loader):
    # Create some symbols
    symbols = [
        parse_symbol(
            "scip-python python automata v0.0.0 `my_project.core.calculator`/Calculator#__init__()."
        ),
        parse_symbol(
            "scip-python python automata v0.0.0 `my_project.core.calculator`/Calculator#add()."
        ),
        parse_symbol("scip-python python automata v0.0.0 `my_project.core.calculator`#"),
        parse_symbol(
            "scip-python python automata v0.0.0 `my_project.core.calculator2`/Calculator2#__init__()."
        ),
        parse_symbol(
            "scip-python python automata v0.0.0 `my_project.core.calculator2`/Calculator2#__add__()."
        ),
        parse_symbol("scip-python python automata v0.0.0 `my_project.core.calculator2`#"),
        parse_symbol(
            "scip-python python automata v0.0.0 `my_project.core.extended.calculator3`/Calculator3#__init__()."
        ),
        parse_symbol(
            "scip-python python automata v0.0.0 `my_project.core.extended.calculator3`/Calculator3#__add__()."
        ),
        parse_symbol("scip-python python automata v0.0.0 `my_project.core.extended.calculator3`#"),
        parse_symbol(  # include a symbol that will be ignored, e.g. not a method or class
            "scip-python python automata v0.0.0 `my_project.core.extended.calculator3`/Calculator3#__add__().(self)"
        ),
    ]

    filtered_symbols = get_rankable_symbols(
        symbols,
    )

    assert len(filtered_symbols) == 9

    filtered_symbols_no_calculator2 = get_rankable_symbols(
        symbols,
        symbols_strings_to_filter=["calculator2"],
    )

    assert len(filtered_symbols_no_calculator2) == 6
