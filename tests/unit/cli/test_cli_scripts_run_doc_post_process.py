from unittest.mock import MagicMock, patch

import pytest

from automata.code_writers.py.doc_writer import PyDocWriter
from automata.singletons.dependency_factory import DependencyFactory
from automata.symbol_embedding import SymbolDocEmbedding


@pytest.fixture
def mock_initialize_modules():
    def _initialize_modules(*args, **kwargs):
        if (
            "project_name" in kwargs
            and kwargs["project_name"] != "test_project"
        ):
            raise ValueError(
                "Incorrect project_name argument received by initialize_py_module_loader"
            )

    with patch("automata.cli.cli_utils.initialize_py_module_loader") as mock:
        mock.side_effect = _initialize_modules
        yield mock


@pytest.fixture
def mock_pydocwriter():
    with patch("automata.code_parsers.py.PyDocWriter") as mock:
        mock.return_value = MagicMock(spec=PyDocWriter)
        yield mock


@pytest.fixture
def mock_get_root_fpath():
    with patch("automata.core.utils.get_root_fpath") as mock:
        mock.return_value = "/path/to/project/root"
        yield mock


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
    mock_get_root_fpath,
    mock_chromasymbolembeddingvectordatabase,
):
    return {
        "mock_initialize_modules": mock_initialize_modules,
        "mock_pydocwriter": mock_pydocwriter,
        "mock_get_root_fpath": mock_get_root_fpath,
        "mock_chromasymbolembeddingvectordatabase": mock_chromasymbolembeddingvectordatabase,
    }


@pytest.mark.skip("Fixme")
def test_main_without_kwargs(main_dependencies):
    from automata.cli.scripts.run_doc_post_process import main

    result = main()
    assert result == "Success"

    main_dependencies["mock_initialize_modules"].assert_called_once_with()
    main_dependencies["mock_pydocwriter"].assert_called_once_with(
        "/path/to/project/root"
    )
    main_dependencies[
        "mock_chromasymbolembeddingvectordatabase"
    ].assert_called_once_with(
        "automata",
        persist_directory=DependencyFactory.DEFAULT_DOC_EMBEDDING_FPATH,
        factory=SymbolDocEmbedding.from_args,
    )


@pytest.mark.skip(reason="Test not implemented yet")
def test_main_with_kwargs(main_dependencies):
    from automata.cli.scripts.run_doc_post_process import main

    result = main(project_name="test_project")
    assert result == "Success"

    main_dependencies["mock_initialize_modules"].assert_called_once_with(
        project_name="test_project"
    )
    main_dependencies["mock_pydocwriter"].assert_called_once_with(
        "/path/to/project/root"
    )
    main_dependencies[
        "mock_chromasymbolembeddingvectordatabase"
    ].assert_called_once_with(
        "test_project",
        persist_directory=DependencyFactory.DEFAULT_DOC_EMBEDDING_FPATH,
        factory=SymbolDocEmbedding.from_args,
    )
