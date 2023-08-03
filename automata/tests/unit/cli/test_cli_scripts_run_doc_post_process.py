from unittest.mock import MagicMock, patch

import pytest

from automata.code_writers.py.py_doc_writer import PyDocWriter
from automata.singletons.dependency_factory import DependencyFactory
from automata.singletons.py_module_loader import PyModuleLoader
from automata.symbol_embedding import SymbolDocEmbedding


@pytest.fixture
def mock_initialize_modules():
    with patch("automata.cli.cli_utils.initialize_py_module_loader") as mock:
        yield mock


@pytest.fixture
def mock_pydocwriter():
    with patch.object(
        PyDocWriter, "write_documentation", new_callable=MagicMock
    ):
        yield PyDocWriter


@pytest.fixture
def mock_chromasymbolembeddingvectordatabase():
    with patch(
        "automata.symbol_embedding.ChromaSymbolEmbeddingVectorDatabase"
    ) as mock:
        instance = mock.return_value
        instance.get_all_ordered_embeddings.return_value = [
            MagicMock(spec=SymbolDocEmbedding)
        ]
        yield mock


@pytest.fixture
def main_dependencies(
    mock_initialize_modules,
    mock_pydocwriter,
    mock_chromasymbolembeddingvectordatabase,
):
    return {
        "mock_initialize_modules": mock_initialize_modules,
        "mock_pydocwriter": mock_pydocwriter,
        "mock_chromasymbolembeddingvectordatabase": mock_chromasymbolembeddingvectordatabase,
    }


def test_main_without_kwargs(main_dependencies, mock_pydocwriter):
    from automata.cli.scripts.run_doc_post_process import main

    PyModuleLoader().reset()

    result = main()
    assert result == "Success"

    mock_pydocwriter.write_documentation.assert_called()


def test_main_with_kwargs(main_dependencies):
    from automata.cli.scripts.run_doc_post_process import main

    PyModuleLoader().reset()

    project_name = "test_project"
    result = main(project_name=project_name)
    assert result == "Success"
