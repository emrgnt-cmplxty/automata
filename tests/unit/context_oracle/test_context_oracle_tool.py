from unittest.mock import MagicMock

import pytest

from automata.tools.base import Tool
from automata.tools.builders.context_oracle import ContextOracleToolkitBuilder


@pytest.fixture
def context_oracle_tool_builder():
    symbol_search = MagicMock()
    symbol_code_embedding_handler = MagicMock()
    symbol_doc_embedding_handler = MagicMock()
    embedding_similarity_calculator = MagicMock()

    return ContextOracleToolkitBuilder(
        symbol_search=symbol_search,
        symbol_doc_embedding_handler=symbol_doc_embedding_handler,
        symbol_code_embedding_handler=symbol_code_embedding_handler,
        embedding_similarity_calculator=embedding_similarity_calculator,
    )


def test_init(context_oracle_tool_builder):
    assert isinstance(context_oracle_tool_builder.embedding_similarity_calculator, MagicMock)
    assert isinstance(context_oracle_tool_builder.symbol_doc_embedding_handler, MagicMock)
    assert isinstance(context_oracle_tool_builder.symbol_code_embedding_handler, MagicMock)


def test_build(context_oracle_tool_builder):
    tools = context_oracle_tool_builder.build()
    assert len(tools) == 1
    for tool in tools:
        assert isinstance(tool, Tool)
