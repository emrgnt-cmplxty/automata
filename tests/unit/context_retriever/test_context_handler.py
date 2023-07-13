import os
from unittest.mock import MagicMock

import pytest

from automata.code_parsers.py import (
    ContextComponent,
    PyContextHandler,
    PyContextHandlerConfig,
    PyContextRetriever,
)
from automata.core.utils import get_root_fpath
from automata.experimental.search import SymbolSearch
from automata.singletons.py_module_loader import py_module_loader
from automata.symbol import Symbol, parse_symbol


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
def context_handler():
    config = PyContextHandlerConfig(top_n_symbol_rank_matches=3, top_n_dependency_matches=3)
    retriever = PyContextRetriever()
    symbol_search = MagicMock()
    return PyContextHandler(config, retriever, symbol_search)


def test_construct_symbol_context(context_handler):
    symbol = parse_symbol(
        "scip-python python automata v0.0.0 `my_project.core.calculator`/Calculator#"
    )
    primary_active_components = {ContextComponent.HEADLINE: {}, ContextComponent.INTERFACE: {}}
    tertiary_active_components = {ContextComponent.HEADLINE: {}}

    context_handler.symbol_search.get_symbol_rank_results.return_value = [
        (
            parse_symbol(
                "scip-python python automata v0.0.0 `my_project.core.calculator2`/Calculator2#"
            ),
            0.8,
        )
    ] * context_handler.config.top_n_symbol_rank_matches
    context_handler.symbol_search.get_symbol_dependencies.return_value = set(
        [
            parse_symbol(
                "scip-python python automata v0.0.0 `my_project.core.extended.calculator3`/Calculator3#"
            )
        ]
        * context_handler.config.top_n_dependency_matches
    )

    context = context_handler.construct_symbol_context(
        symbol, primary_active_components, tertiary_active_components
    )
    # print("context = ", context)
    # assert False
    assert "Primary Symbols:" in context
    assert "Building symbol context:" in context
    assert "Interface:" in context
    assert "Primary Symbols:" in context
    assert "Dependent Symbols:" in context


def test_get_top_n_symbol_rank_matches(context_handler):
    symbol = parse_symbol(
        "scip-python python automata v0.0.0 `my_project.core.calculator`/Calculator#"
    )
    top_symbols = context_handler.get_top_n_symbol_rank_matches(symbol)
    assert len(top_symbols) == context_handler.config.top_n_symbol_rank_matches
    assert all(isinstance(s, Symbol) for s in top_symbols)


def test_get_top_n_symbol_dependencies(context_handler):
    symbol = parse_symbol(
        "scip-python python automata v0.0.0 `my_project.core.calculator`/Calculator#"
    )
    top_dependencies = context_handler.get_top_n_symbol_dependencies(symbol)
    assert len(top_dependencies) == context_handler.config.top_n_dependency_matches
    assert all(isinstance(s, Symbol) for s in top_dependencies)
