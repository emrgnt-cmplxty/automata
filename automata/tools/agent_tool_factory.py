"""The `AgentToolFactory` class is responsible for creating tools from a given agent tool name."""
# TODO - Move experimental tools to a separate package
import logging
from typing import Any, Dict, List, Sequence, Tuple

from automata.agent import AgentToolkitNames
from automata.code_parsers.py import PyReader
from automata.code_writers.py import PyCodeWriter
from automata.config.config_base import LLMProvider
from automata.embedding import EmbeddingSimilarityCalculator
from automata.experimental.memory_store import SymbolDocEmbeddingHandler
from automata.experimental.search import SymbolSearch
from automata.memory_store import SymbolCodeEmbeddingHandler
from automata.tools import Tool, UnknownToolError

logger = logging.getLogger(__name__)


class AgentToolFactory:
    """The AgentToolFactory class is responsible for creating tools from a given agent tool name."""

    TOOLKIT_TYPE_TO_ARGS: Dict[AgentToolkitNames, List[Tuple[str, Any]]] = {
        AgentToolkitNames.SYMBOL_SEARCH: [("symbol_search", SymbolSearch)],
        AgentToolkitNames.ADVANCED_CONTEXT_ORACLE: [
            ("symbol_search", SymbolSearch),
            ("symbol_doc_embedding_handler", SymbolDocEmbeddingHandler),
            ("symbol_code_embedding_handler", SymbolCodeEmbeddingHandler),
            ("embedding_similarity_calculator", EmbeddingSimilarityCalculator),
        ],
        AgentToolkitNames.DOCUMENT_ORACLE: [
            ("symbol_search", SymbolSearch),
            ("symbol_doc_embedding_handler", SymbolDocEmbeddingHandler),
        ],
        AgentToolkitNames.PY_READER: [("py_reader", PyReader)],
        AgentToolkitNames.PY_WRITER: [("py_writer", PyCodeWriter)],
        AgentToolkitNames.AGENTIFIED_SEARCH: [
            ("symbol_search", SymbolSearch),
            ("symbol_doc_embedding_handler", SymbolDocEmbeddingHandler),
        ],
    }

    @staticmethod
    def create_tools_from_builder(
        agent_tool: AgentToolkitNames, **kwargs
    ) -> Sequence[Tool]:
        """Uses the Builder Registry to create tools from a given agent tool name."""
        from automata.singletons.toolkit_registry import (  # import here for easy mocking
            OpenAIAutomataAgentToolkitRegistry,
        )

        for builder in OpenAIAutomataAgentToolkitRegistry.get_all_builders():
            if builder.can_handle(agent_tool):
                if builder.LLM_PROVIDER == LLMProvider.OPENAI:
                    return builder(**kwargs).build_for_open_ai()
                else:
                    return builder(**kwargs).build()

        raise UnknownToolError(agent_tool.value)

    @staticmethod
    def build_tools(toolkits: List[str], **kwargs) -> List[Tool]:
        """Given a list of tools this method builds the tools and returns them."""
        tools: List[Tool] = []

        for tool_name in toolkits:
            tool_name = tool_name.strip()
            agent_tool_manager = AgentToolkitNames(tool_name)

            if agent_tool_manager is None:
                raise UnknownToolError(agent_tool_manager)

            tools.extend(
                AgentToolFactory.create_tools_from_builder(
                    agent_tool_manager, **kwargs
                )
            )

        return tools
