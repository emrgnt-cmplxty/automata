import os
import random
from unittest.mock import Mock

import pytest

from automata.tools.search.symbol_parser import parse_uri_to_symbol


@pytest.fixture
def temp_output_filename():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(this_dir, "test_output.json")
    yield filename
    if os.path.exists(filename):
        os.remove(filename)


@pytest.fixture
def mock_embedding(monkeypatch):
    return [random.random() for _ in range(1024)]


prefix = "scip-python python automata 75482692a6fe30c72db516201a6f47d9fb4af065 `automata.configs.automata_agent_configs`/"


@pytest.fixture
def mock_simple_method_symbols(monkeypatch):
    return [
        parse_uri_to_symbol(prefix + str(random.random()) + "_uri_ex_method().")
        for _ in range(100)
    ]


@pytest.fixture
def mock_simple_class_symbols():
    return [
        parse_uri_to_symbol(prefix + str(random.random()) + "_uri_ex_method#") for _ in range(100)
    ]


@pytest.fixture
def mock_symbol_converter():
    mock_symbol_converter = Mock()
    mock_symbol_converter.convert_to_fst_object.return_value = "symbol_source"
    return mock_symbol_converter
