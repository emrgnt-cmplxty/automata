import logging
import os
from typing import Dict, List

from automata.config.config_types import ConfigCategory
from automata.core.agent.tools.agent_tool import AgentTool
from automata.core.agent.tools.py_code_retriever import PyCodeRetrieverTool
from automata.core.agent.tools.py_code_writer import PyCodeWriterTool
from automata.core.agent.tools.symbol_search import SymbolSearchTool
from automata.core.base.tool import Tool, Toolkit, ToolkitType
from automata.core.coding.py_coding.retriever import PyCodeRetriever
from automata.core.coding.py_coding.writer import PyCodeWriter
from automata.core.database.vector import JSONVectorDatabase
from automata.core.embedding.code_embedding import SymbolCodeEmbeddingHandler
from automata.core.embedding.embedding_types import OpenAIEmbedding
from automata.core.embedding.symbol_similarity import SymbolSimilarity
from automata.core.symbol.graph import SymbolGraph
from automata.core.symbol.search.rank import SymbolRankConfig
from automata.core.symbol.search.symbol_search import SymbolSearch
from automata.core.utils import config_fpath

logger = logging.getLogger(__name__)


class ToolManagerFactory:
    """
    A class for creating tool managers.
    """

    _retriever_instance = None

    @staticmethod
    def create_tool_manager(toolkit_type: ToolkitType) -> AgentTool:
        if toolkit_type == ToolkitType.PYTHON_RETRIEVER:
            if ToolManagerFactory._retriever_instance is None:
                ToolManagerFactory._retriever_instance = PyCodeRetriever()
            return PyCodeRetrieverTool(python_retriever=ToolManagerFactory._retriever_instance)
        elif toolkit_type == ToolkitType.PYTHON_WRITER:
            if ToolManagerFactory._retriever_instance is None:
                ToolManagerFactory._retriever_instance = PyCodeRetriever()
            return PyCodeWriterTool(
                python_writer=PyCodeWriter(ToolManagerFactory._retriever_instance)
            )
        elif toolkit_type == ToolkitType.SYMBOL_SEARCHER:
            graph = SymbolGraph()
            subgraph = graph.get_rankable_symbol_subgraph()

            code_embedding_fpath = os.path.join(
                config_fpath(), ConfigCategory.SYMBOL.value, "symbol_code_embedding.json"
            )
            code_embedding_db = JSONVectorDatabase(code_embedding_fpath)
            code_embedding_handler = SymbolCodeEmbeddingHandler(
                code_embedding_db, OpenAIEmbedding()
            )

            symbol_similarity = SymbolSimilarity(code_embedding_handler)
            symbol_search = SymbolSearch(
                graph,
                symbol_similarity,
                symbol_rank_config=SymbolRankConfig(),
                code_subgraph=subgraph,
            )
            return SymbolSearchTool(symbol_search=symbol_search)
        else:
            raise ValueError("Unknown toolkit type: %s" % toolkit_type)


class ToolkitBuilder:
    def __init__(self, **kwargs):
        """Initializes a ToolkitBuilder object with the given inputs."""

        self._tool_management: Dict[ToolkitType, AgentTool] = {}

    def _build_toolkit(self, toolkit_type: ToolkitType) -> Toolkit:
        """Builds a toolkit of the given type."""
        tool_manager = ToolManagerFactory.create_tool_manager(toolkit_type)

        if not tool_manager:
            raise ValueError("Unknown toolkit type: %s" % toolkit_type)
        tools = ToolkitBuilder.build(tool_manager)
        return Toolkit(tools)

    @staticmethod
    def build(tool_manager: AgentTool) -> List[Tool]:
        """Build tools from a tool manager."""
        return tool_manager.build()


def build_llm_toolkits(tool_list: List[str], **kwargs) -> Dict[ToolkitType, Toolkit]:
    toolkits: Dict[ToolkitType, Toolkit] = {}
    toolkit_builder = ToolkitBuilder(**kwargs)
    for tool_name in tool_list:
        tool_name = tool_name.strip()
        toolkit_type = None
        if tool_name == "python_retriever":
            toolkit_type = ToolkitType.PYTHON_RETRIEVER
        elif tool_name == "python_writer":
            toolkit_type = ToolkitType.PYTHON_WRITER
        elif tool_name == "symbol_searcher":
            toolkit_type = ToolkitType.SYMBOL_SEARCHER
        else:
            logger.warning("Unknown tool: %s", tool_name)
            continue

        toolkit = toolkit_builder._build_toolkit(toolkit_type)  # type: ignore
        toolkits[toolkit_type] = toolkit

    return toolkits
