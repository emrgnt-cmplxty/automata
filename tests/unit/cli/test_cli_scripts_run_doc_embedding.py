from unittest.mock import MagicMock, patch

import pytest

from automata.cli.scripts.run_doc_embedding import initialize_providers, main
from automata.symbol.base import SymbolDescriptor


class FakeSymbol:
    def __init__(
        self,
        full_dotpath,
        uri="some_uri",
        py_kind=SymbolDescriptor.PyKind.Method,
        is_protobuf=False,
        is_local=False,
        is_meta=False,
        is_parameter=False,
    ):
        self.full_dotpath = full_dotpath
        self.uri = uri
        self.py_kind = py_kind
        self.is_protobuf = is_protobuf
        self.is_local = is_local
        self.is_meta = is_meta
        self.is_parameter = is_parameter


@pytest.fixture
def symbol_graph_mock():
    mock = MagicMock()
    mock.get_sorted_supported_symbols.return_value = [
        FakeSymbol("symbol1"),
        FakeSymbol("symbol2"),
    ]
    return mock


@pytest.fixture
def symbol_doc_embedding_handler_mock():
    mock = MagicMock()
    mock.process_embedding.side_effect = Exception("Test exception")
    return mock


@patch("automata.cli.scripts.run_doc_embedding.SymbolGraph")
@patch(
    "automata.cli.scripts.run_doc_embedding.ChromaSymbolEmbeddingVectorDatabase"
)
@patch("automata.cli.scripts.run_doc_embedding.OpenAIEmbeddingProvider")
@patch(
    "automata.cli.scripts.run_doc_embedding.DependencyFactory.set_overrides"
)
@patch("automata.cli.scripts.run_doc_embedding.DependencyFactory.get")
@pytest.mark.skip("Fixme")
def test_initialize_providers(
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
    symbol_code_embedding_handler = MagicMock()
    symbol_code_embedding_handler._get_sorted_supported_symbols.return_value = [
        FakeSymbol("symbol1"),
        FakeSymbol("symbol2"),
    ]
    symbol_doc_embedding_handler = MagicMock()
    get_mock.side_effect = [
        symbol_code_embedding_handler,
        symbol_doc_embedding_handler,
    ]
    symbol_doc_embedding_handler.is_synchronized = True

    symbol_graph_mock._get_sorted_supported_symbols.return_value = (
        symbol_code_embedding_handler._get_sorted_supported_symbols.return_value
    )

    symbol_doc_embedding_handler, filtered_symbols = initialize_providers(
        embedding_level=2, project_name="test_project"
    )

    assert symbol_doc_embedding_handler.is_synchronized
    assert filtered_symbols

    overrides = {
        "symbol_graph": symbol_graph_mock,
        "code_embedding_db": ChromaSymbolEmbeddingVectorDatabase_mock.return_value,
        "doc_embedding_db": ChromaSymbolEmbeddingVectorDatabase_mock.return_value,
        "embedding_provider": OpenAIEmbeddingProvider_mock.return_value,
        "disable_synchronization": True,
    }
    set_overrides_mock.assert_called_once_with(**overrides)


@patch("automata.cli.scripts.run_doc_embedding.initialize_providers")
def test_main(initialize_providers_mock, symbol_doc_embedding_handler_mock):
    symbol_mock = MagicMock()
    initialize_providers_mock.return_value = (
        symbol_doc_embedding_handler_mock,
        [symbol_mock],
    )

    result = main()

    assert result == "Success"
    initialize_providers_mock.assert_called_once()
    symbol_doc_embedding_handler_mock.process_embedding.assert_called_once_with(
        symbol_mock
    )
