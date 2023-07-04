from unittest.mock import MagicMock

import pytest

from automata.core.tools.base import Tool
from automata.core.tools.builders.context_oracle import ContextOracleToolkitBuilder


@pytest.fixture
def context_oracle_tool_builder():
    symbol_doc_embedding_handler = MagicMock()
    symbol_code_embedding_handler = MagicMock()
    embedding_similarity_calculator = MagicMock()

    return ContextOracleToolkitBuilder(
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


# def test_context_generator(context_oracle_tool_builder):
#     context_oracle_tool_builder.symbol_doc_similarity.calculate_query_similarity_dict = MagicMock(
#         return_value={"doc1": 0.9, "doc2": 0.8}
#     )
#     context_oracle_tool_builder.symbol_doc_similarity.embedding_handler.get_embedding = MagicMock(
#         return_value=SymbolDocEmbedding(symbol="x", document="y", source_code="z", vector=[0, 1])
#     )
#     context_oracle_tool_builder.symbol_code_similarity.embedding_handler.get_embedding = MagicMock(
#         return_value=SymbolDocEmbedding(symbol="x", document="y", source_code="z", vector=[0, 1])
#     )

#     tools = context_oracle_tool_builder.build()
#     for tool in tools:
#         if tool.name == "context-oracle":
#             assert tool.function(("query", 5)) == "zy"  # TODO - Investigate why this is the result
