from unittest.mock import MagicMock, patch

import pytest

from automata.cli.scripts.run_code_embedding import (
    collect_symbols,
    initialize_resources,
    logger,
    main,
    process_embeddings,
)


@pytest.fixture
def symbol_graph_mock():
    return MagicMock()


@pytest.fixture
def symbol_code_embedding_handler_mock():
    mock = MagicMock()
    mock.process_embedding.side_effect = Exception("Test exception")
    return mock


@patch("automata.cli.scripts.run_code_embedding.SymbolGraph")
@patch(
    "automata.cli.scripts.run_code_embedding.ChromaSymbolEmbeddingVectorDatabase"
)
@patch("automata.cli.scripts.run_code_embedding.OpenAIEmbeddingProvider")
@patch(
    "automata.cli.scripts.run_code_embedding.DependencyFactory.set_overrides"
)
@patch("automata.cli.scripts.run_code_embedding.DependencyFactory.get")
@pytest.mark.skip("Fixme")
def test_initialize_resources(
    get_mock,
    set_overrides_mock,
    OpenAIEmbeddingProvider_mock,
    ChromaSymbolEmbeddingVectorDatabase_mock,
    SymbolGraph_mock,
    symbol_graph_mock,
):
    SymbolGraph_mock.return_value = symbol_graph_mock
    ChromaSymbolEmbeddingVectorDatabase_mock.return_value = MagicMock()
    OpenAIEmbeddingProvider_mock.return_value = MagicMock()
    get_mock.return_value = MagicMock()

    symbol_graph, symbol_code_embedding_handler = initialize_resources(
        "test_project"
    )

    assert symbol_graph.is_synchronized
    assert symbol_code_embedding_handler.is_synchronized

    overrides = {
        "symbol_graph": symbol_graph_mock,
        "code_embedding_db": ChromaSymbolEmbeddingVectorDatabase_mock.return_value,
        "embedding_provider": OpenAIEmbeddingProvider_mock.return_value,
        "disable_synchronization": True,
    }
    set_overrides_mock.assert_called_once_with(**overrides)


@pytest.mark.parametrize(
    "py_kind,is_protobuf,is_local,is_meta,is_parameter",
    [
        ("Method", False, False, False, False),
        ("Other", False, False, False, False),
        ("Method", True, False, False, False),
    ],
)
@patch(
    "automata.cli.scripts.run_code_embedding.get_rankable_symbols",
    side_effect=lambda x: x,
)
def test_collect_symbols(
    get_rankable_symbols_mock,
    py_kind,
    is_protobuf,
    is_local,
    is_meta,
    is_parameter,
    symbol_graph_mock,
):
    mock_symbol = MagicMock()
    mock_symbol.full_dotpath = "test_path"
    mock_symbol.uri = "test_uri"
    mock_symbol.py_kind = py_kind
    mock_symbol.is_protobuf = is_protobuf
    mock_symbol.is_local = is_local
    mock_symbol.is_meta = is_meta
    mock_symbol.is_parameter = is_parameter

    symbol_graph_mock.get_sorted_supported_symbols.return_value = [mock_symbol]

    filtered_symbols = collect_symbols(symbol_graph_mock)

    assert filtered_symbols


@patch("automata.cli.scripts.run_code_embedding.tqdm")
def test_process_embeddings(tqdm_mock, symbol_code_embedding_handler_mock):
    symbol_mock = MagicMock()
    symbol_mock.full_dotpath = "test_path"
    tqdm_mock.return_value = [symbol_mock]

    process_embeddings(symbol_code_embedding_handler_mock, [symbol_mock])

    symbol_code_embedding_handler_mock.process_embedding.assert_called_once_with(
        symbol_mock
    )
    symbol_code_embedding_handler_mock.flush.assert_called_once()


@patch("automata.cli.scripts.run_code_embedding.initialize_py_module_loader")
@patch("automata.cli.scripts.run_code_embedding.initialize_resources")
@patch("automata.cli.scripts.run_code_embedding.collect_symbols")
@patch("automata.cli.scripts.run_code_embedding.process_embeddings")
def test_main_1(
    process_embeddings_mock,
    collect_symbols_mock,
    initialize_resources_mock,
    initialize_modules_mock,
    symbol_graph_mock,
    symbol_code_embedding_handler_mock,
):
    initialize_resources_mock.return_value = (
        symbol_graph_mock,
        symbol_code_embedding_handler_mock,
    )
    collect_symbols_mock.return_value = [MagicMock()]

    result = main(project_name="test_project")

    assert result == "Success"
    initialize_modules_mock.assert_called_once()
    initialize_resources_mock.assert_called_once_with(
        project_name="test_project"
    )

    collect_symbols_mock.assert_called_once_with(symbol_graph_mock)
    process_embeddings_mock.assert_called_once_with(
        symbol_code_embedding_handler_mock, collect_symbols_mock.return_value
    )


@patch("automata.cli.scripts.run_code_embedding.tqdm")
def test_process_embeddings_exception(
    tqdm_mock, symbol_code_embedding_handler_mock
):
    symbol_mock = MagicMock()
    symbol_mock.full_dotpath = "test_path"
    tqdm_mock.return_value = [symbol_mock]

    with patch.object(logger, "error") as logger_error_mock:
        process_embeddings(symbol_code_embedding_handler_mock, [symbol_mock])
        logger_error_mock.assert_called_once_with(
            f"Failed to update embedding for {symbol_mock.full_dotpath}: Test exception"
        )

    symbol_code_embedding_handler_mock.flush.assert_called_once()
