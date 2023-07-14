from unittest.mock import MagicMock, Mock, call, patch

import pytest

from automata.cli.scripts.run_code_embedding import (
    collect_symbols,
    initialize_resources,
    main,
    process_embeddings,
)
from automata.memory_store import SymbolCodeEmbeddingHandler
from automata.symbol import Symbol


@pytest.mark.skip(reason="Test not implemented yet")
@patch("builtins.open", new_callable=MagicMock)
@patch(
    "automata.symbol.SymbolGraph._load_index_protobuf", return_value=Mock()
)  # Mock _load_index_protobuf
@patch("automata.llm.OpenAIEmbeddingProvider")
@patch("automata.symbol_embedding.ChromaSymbolEmbeddingVectorDatabase")
@patch("automata.symbol.SymbolGraph", return_value=Mock())
@patch(
    "automata.singletons.dependency_factory.dependency_factory.set_overrides"
)
@patch("automata.singletons.dependency_factory.dependency_factory.get")
def test_initialize_resources(
    mock_get,
    mock_set_overrides,
    mock_symbol_graph,
    mock_db,
    mock_provider,
    _,
    mock_open,
):
    mock_open.return_value.read.return_value = (
        b""  # mock_open.read() returns bytes
    )
    symbol_graph, handler = initialize_resources("project_name")

    mock_get.assert_called_once_with("config")
    mock_set_overrides.assert_called_once_with(
        mock_provider.return_value, mock_db.return_value
    )
    assert isinstance(
        symbol_graph, Mock
    )  # the mock object returned by SymbolGraph()
    assert isinstance(handler, SymbolCodeEmbeddingHandler)


@pytest.mark.skip(reason="Test not implemented yet")
def test_collect_symbols():
    symbol_graph = Mock()
    symbol = Mock(spec=Symbol)  # Create mock symbol objects
    symbol.uri = "symbol_uri"
    symbol.full_dotpath = (
        "symbol1"  # Add additional attribute needed by your function
    )
    symbol_graph.get_sorted_supported_symbols.return_value = [
        symbol,
        symbol,
        symbol,
    ]
    symbol_graph.all_defined_symbols = {
        "symbol1": symbol
    }  # Mock attribute all_defined_symbols
    filtered_symbols = collect_symbols(symbol_graph)
    assert [s.full_dotpath for s in filtered_symbols] == [
        "symbol1",
        "symbol1",
        "symbol1",
    ]


@pytest.mark.skip(reason="Test not implemented yet")
@patch(
    "automata.cli.scripts.run_code_embedding.main", return_value="Success"
)  # Mock main function to return 'Success'
@patch(
    "automata.cli.scripts.run_code_embedding.initialize_resources",
    return_value=(Mock(), Mock()),
)
@patch(
    "automata.cli.scripts.run_code_embedding.collect_symbols",
    return_value=[Mock(spec=Symbol)],
)
@patch("automata.cli.scripts.run_code_embedding.process_embeddings")
@patch("automata.cli.cli_utils.initialize_modules")
def test_main(
    mock_initialize, mock_process, mock_collect, mock_resources, mock_main
):
    main()
    mock_initialize.assert_has_calls(
        [call()]
    )  # ensure initialize_modules is called
    mock_resources.assert_called_once()
    mock_collect.assert_called_once()
    mock_process.assert_called_once()
