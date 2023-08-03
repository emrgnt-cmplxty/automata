import os
from unittest.mock import MagicMock, PropertyMock, patch

import pytest

from automata.cli.scripts.run_code_embedding import (
    collect_symbols,
    initialize_resources,
    logger,
    main,
    process_embeddings,
)
from automata.singletons.dependency_factory import DependencyFactory
from automata.singletons.py_module_loader import py_module_loader
from automata.symbol.graph.symbol_graph import SymbolGraph
from automata.symbol_embedding import SymbolCodeEmbedding


@pytest.fixture
def symbol_graph_mock():
    mock = MagicMock()
    type(mock).is_synchronized = PropertyMock(return_value=True)
    return mock


@pytest.fixture
def symbol_code_embedding_handler_mock():
    mock = MagicMock()
    type(mock).is_synchronized = PropertyMock(return_value=True)
    mock.process_embedding.side_effect = Exception("Test exception")
    return mock


@pytest.mark.skip(
    "Fixme"
)  # TODO - Investigate why this test is acting strangely.
@pytest.mark.parametrize(
    "project_name", ["test_project", "another_test_project"]
)
@patch("automata.llm.OpenAIEmbeddingProvider")
@patch("automata.memory_store.SymbolCodeEmbeddingHandler")
@patch("automata.symbol_embedding.ChromaSymbolEmbeddingVectorDatabase")
@patch("automata.symbol.SymbolGraph.__new__")
@patch("automata.singletons.dependency_factory.dependency_factory")
@patch(
    "automata.symbol.graph.symbol_graph._load_index_protobuf",
    return_value=MagicMock(),
)
def test_initialize_resources(
    load_index_protobuf_mock,
    dependency_factory_mock,
    symbol_graph_mock,
    chroma_db_class_mock,
    embedding_provider_class_mock,
    symbol_code_embedding_handler_class_mock,
    project_name,
):
    # Prepare
    symbol_graph_instance = MagicMock()
    symbol_graph_instance.is_synchronized = True
    symbol_graph_mock.return_value = symbol_graph_instance

    symbol_code_embedding_handler_mock = MagicMock()
    symbol_code_embedding_handler_mock.is_synchronized = True
    symbol_code_embedding_handler_class_mock.return_value = (
        symbol_code_embedding_handler_mock
    )

    original_os_path_join = os.path.join

    symbol_graph, symbol_code_embedding_handler = initialize_resources(
        project_name
    )

    # Assert
    # Get the first argument with which symbol_graph_mock was called
    called_with_args = symbol_graph_mock.call_args[0]
    assert called_with_args[0] == SymbolGraph
    assert isinstance(
        called_with_args[1], str
    )  # check if the second argument is a string
    assert (
        ".scip" in called_with_args[1]
    )  # check if the second argument includes '.scip'

    assert symbol_graph.is_synchronized
    assert symbol_code_embedding_handler.is_synchronized


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
    mock_symbol.dotpath = "test_path"
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
    symbol_mock.dotpath = "test_path"
    tqdm_mock.return_value = [symbol_mock]

    process_embeddings(symbol_code_embedding_handler_mock, [symbol_mock])

    symbol_code_embedding_handler_mock.process_embedding.assert_called_once_with(
        symbol_mock
    )
    symbol_code_embedding_handler_mock.flush.assert_called_once()


@pytest.mark.skip(
    "Fixme"
)  # TODO - Investigate why this test is acting strangely.
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
    py_module_loader.reset()
    py_module_loader.initialize()
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
    symbol_mock.dotpath = "test_path"
    tqdm_mock.return_value = [symbol_mock]

    with patch.object(logger, "error") as logger_error_mock:
        process_embeddings(symbol_code_embedding_handler_mock, [symbol_mock])
        logger_error_mock.assert_called_once_with(
            f"Failed to update embedding for {symbol_mock.dotpath}: Test exception"
        )

    symbol_code_embedding_handler_mock.flush.assert_called_once()
