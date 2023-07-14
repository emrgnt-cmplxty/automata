from unittest.mock import MagicMock, mock_open, patch

import pytest

from automata.cli.scripts.run_doc_embedding import initialize_providers, main


@pytest.mark.skip(reason="Test not implemented yet")
@patch("automata.cli.scripts.run_doc_embedding.initialize_modules")
@patch("automata.cli.scripts.run_doc_embedding.SymbolGraph")
@patch(
    "automata.cli.scripts.run_doc_embedding.ChromaSymbolEmbeddingVectorDatabase"
)
@patch("automata.cli.scripts.run_doc_embedding.OpenAIEmbeddingProvider")
@patch(
    "automata.cli.scripts.run_doc_embedding.dependency_factory.set_overrides"
)
@patch("os.path.join", return_value="mock_directory")
@patch("builtins.open", new_callable=mock_open, read_data=b"binary data")
def test_initialize_providers(
    mock_open_file,
    mock_path_join,
    mock_set_overrides,
    mock_provider,
    mock_db,
    mock_symbol_graph,
    mock_initialize,
):
    symbol_handler, filtered_symbols = initialize_providers(
        embedding_level=2, project_name="test"
    )
    mock_initialize.assert_called_once()
    mock_symbol_graph.assert_called_once()
    mock_db.assert_called()
    mock_provider.assert_called_once()
    mock_set_overrides.assert_called_once()
    mock_path_join.assert_called()


@patch("automata.cli.scripts.run_doc_embedding.initialize_providers")
@patch("automata.cli.scripts.run_doc_embedding.tqdm")
def test_main(mock_tqdm, mock_initialize):
    symbol_mock = MagicMock()
    symbol_mock.full_dotpath = "symbol1"
    mock_initialize.return_value = (
        MagicMock(),
        [symbol_mock, symbol_mock, symbol_mock],
    )
    mock_tqdm.return_value = [symbol_mock, symbol_mock, symbol_mock]
    assert main() == "Success"
    mock_tqdm.assert_called_once()
