import os
from unittest.mock import MagicMock

import pytest

from automata.core.utils import get_root_fpath
from automata.experimental.code_parsers import (
    ContextComponent,
    PyContextHandler,
    PyContextHandlerConfig,
    PyContextRetriever,
)
from automata.singletons.py_module_loader import py_module_loader
from automata.symbol import parse_symbol


# TODO - Unify module loader fixture
@pytest.fixture(autouse=True)
def local_module_loader():
    # FIXME - This can't be a good pattern, let's cleanup later.
    py_module_loader.reset()
    py_module_loader.initialize(
        os.path.join(get_root_fpath(), "tests", "unit", "sample_modules"),
        "my_project",
    )
    yield py_module_loader


@pytest.fixture
def context_handler():
    config = PyContextHandlerConfig(
        top_n_symbol_rank_matches=3, top_n_dependency_matches=3
    )
    retriever = PyContextRetriever()
    symbol_search = MagicMock()
    return PyContextHandler(config, retriever, symbol_search)


def test_construct_symbol_context_no_interface(context_handler):
    symbol = parse_symbol(
        "scip-python python automata v0.0.0 `my_project.core.calculator`/Calculator#"
    )
    primary_active_components = {
        ContextComponent.HEADLINE: {},
        ContextComponent.INTERFACE: {},
    }
    tertiary_active_components = {ContextComponent.HEADLINE: {}}

    context_handler.symbol_search.get_symbol_rank_results.return_value = [
        (
            parse_symbol(
                "scip-python python automata v0.0.0 `my_project.core.calculator2`/Calculator2#"
            ),
            0.8,
        )
    ]
    context_handler.symbol_search.symbol_graph.get_symbol_dependencies.return_value = [
        parse_symbol(
            "scip-python python automata v0.0.0 `my_project.core.extended.calculator3`/Calculator3#"
        )
    ]

    context = context_handler.construct_symbol_context(
        symbol, primary_active_components, tertiary_active_components
    )
    assert "Interface:" in context
    assert "add(" in context
    assert "subtract(" in context

    assert "Related Symbols:" in context
    assert "Dependent Symbols:" in context
    assert "my_project.core.calculator2.Calculator2" in context
    assert "my_project.core.extended.calculator3.Calculator3" in context
    assert "add" in context
    assert "add2" not in context
    assert "add3" not in context


def test_construct_symbol_context_interface(context_handler):
    symbol = parse_symbol(
        "scip-python python automata v0.0.0 `my_project.core.calculator`/Calculator#"
    )
    primary_active_components = {
        ContextComponent.HEADLINE: {},
        ContextComponent.INTERFACE: {},
    }
    tertiary_active_components = {
        ContextComponent.HEADLINE: {},
        ContextComponent.INTERFACE: {},
    }

    context_handler.symbol_search.get_symbol_rank_results.return_value = [
        (
            parse_symbol(
                "scip-python python automata v0.0.0 `my_project.core.calculator2`/Calculator2#"
            ),
            0.8,
        )
    ]
    context_handler.symbol_search.symbol_graph.get_symbol_dependencies.return_value = [
        parse_symbol(
            "scip-python python automata v0.0.0 `my_project.core.extended.calculator3`/Calculator3#"
        )
    ]

    context = context_handler.construct_symbol_context(
        symbol, primary_active_components, tertiary_active_components
    )
    assert "Interface:" in context
    assert "add(" in context
    assert "subtract(" in context

    assert "Related Symbols:" in context
    assert "Dependent Symbols:" in context
    assert "my_project.core.calculator2.Calculator2" in context
    assert "my_project.core.extended.calculator3.Calculator3" in context
    assert "add" in context
    assert "add2" in context
    assert "add3" in context
