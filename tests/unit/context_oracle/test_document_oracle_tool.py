from unittest.mock import MagicMock

import pytest

from automata.experimental.tools import DocumentOracleToolkitBuilder
from automata.tools.tool_base import Tool


@pytest.fixture
def symbol_search():
    return MagicMock()


@pytest.fixture
def symbol_code_embedding_handler():
    return MagicMock()


@pytest.fixture
def symbol_doc_embedding_handler():
    return MagicMock()


@pytest.fixture
def embedding_similarity_calculator():
    return MagicMock()


@pytest.fixture
def document_oracle_tool_builder(
    symbol_search,
    symbol_code_embedding_handler,
    symbol_doc_embedding_handler,
    embedding_similarity_calculator,
):
    return DocumentOracleToolkitBuilder(
        symbol_search=symbol_search,
        symbol_doc_embedding_handler=symbol_doc_embedding_handler,
        symbol_code_embedding_handler=symbol_code_embedding_handler,
        embedding_similarity_calculator=embedding_similarity_calculator,
    )


def test_init(document_oracle_tool_builder):
    assert isinstance(
        document_oracle_tool_builder.symbol_doc_embedding_handler,
        MagicMock,
    )


def test_build(document_oracle_tool_builder):
    tools = document_oracle_tool_builder.build()
    assert len(tools) == 1
    for tool in tools:
        assert isinstance(tool, Tool)
