from unittest.mock import MagicMock, Mock, call, patch

import pytest

from automata.cli.scripts.run_code_embedding import main
from automata.memory_store import SymbolCodeEmbeddingHandler
from automata.symbol import Symbol


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
