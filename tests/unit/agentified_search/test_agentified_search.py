import ast
from unittest.mock import MagicMock

from automata.singletons.py_module_loader import py_module_loader
from automata.tools.tool_base import Tool


def test_init(agentified_search_tool_builder):
    assert isinstance(agentified_search_tool_builder.symbol_search, MagicMock)
    assert isinstance(
        agentified_search_tool_builder.symbol_doc_embedding_handler, MagicMock
    )
    assert isinstance(
        agentified_search_tool_builder.completion_provider, MagicMock
    )


def test_build(agentified_search_tool_builder):
    tools = agentified_search_tool_builder.build()
    assert len(tools) == 3
    for tool in tools:
        assert isinstance(tool, Tool)


def test_get_top_matches(agentified_search_tool_builder):
    tools = agentified_search_tool_builder.build()
    for tool in tools:
        if tool.name == "search-top-matches":
            result = tool.function("symbol")
            assert isinstance(result, str)


def test_get_code_for_best_match(agentified_search_tool_builder, monkeypatch):
    py_module_loader.initialize()
    monkeypatch.setattr(
        "automata.symbol.convert_to_ast_object",
        MagicMock(return_value=ast.parse("")),
    )
    monkeypatch.setattr("ast.unparse", MagicMock(return_value="some_code"))

    tools = agentified_search_tool_builder.build()
    for tool in tools:
        if tool.name == "search-best-match-code":
            result = tool.function("symbol")
            assert isinstance(result, str)
            assert result == "some_code"


def test_get_docs_for_best_match(agentified_search_tool_builder):
    agentified_search_tool_builder.symbol_doc_embedding_handler.get_embeddings = MagicMock(
        return_value=[MagicMock()]
    )

    tools = agentified_search_tool_builder.build()
    for tool in tools:
        if tool.name == "search-best-match-docs":
            result = tool.function("symbol")
            assert isinstance(result, str)
