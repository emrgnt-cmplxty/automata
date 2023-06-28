import functools
import logging
import os
from typing import Any, Dict, List, Sequence, Tuple

from automata.config.base import ConfigCategory, LLMProvider
from automata.core.agent.error import AgentGeneralError, UnknownToolError
from automata.core.agent.tool.registry import AutomataOpenAIAgentToolBuilderRegistry
from automata.core.base.agent import AgentToolProviders
from automata.core.base.database.vector import JSONVectorDatabase
from automata.core.base.tool import Tool
from automata.core.coding.py.reader import PyReader
from automata.core.coding.py.writer import PyWriter
from automata.core.context.py.retriever import (
    PyContextRetriever,
    PyContextRetrieverConfig,
)
from automata.core.embedding.code_embedding import SymbolCodeEmbeddingHandler
from automata.core.embedding.doc_embedding import SymbolDocEmbeddingHandler
from automata.core.embedding.symbol_similarity import SymbolSimilarityCalculator
from automata.core.llm.providers.openai import (
    OpenAIChatCompletionProvider,
    OpenAIEmbeddingProvider,
)
from automata.core.symbol.graph import SymbolGraph
from automata.core.symbol.search.rank import SymbolRankConfig
from automata.core.symbol.search.symbol_search import SymbolSearch
from automata.core.utils import get_config_fpath

logger = logging.getLogger(__name__)


def classmethod_lru_cache():
    """Class method LRU cache decorator which caches the return value of a class method."""

    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            cache_key = (func.__name__,) + args + tuple(sorted(kwargs.items()))
            if cache_key not in self._class_cache:
                self._class_cache[cache_key] = func(self, *args, **kwargs)
            return self._class_cache[cache_key]

        return wrapper

    return decorator


class DependencyFactory:
    """Creates dependencies for input Tool construction."""

    DEFAULT_SCIP_FPATH = os.path.join(
        get_config_fpath(), ConfigCategory.SYMBOL.value, "index.scip"
    )

    DEFAULT_CODE_EMBEDDING_FPATH = os.path.join(
        get_config_fpath(), ConfigCategory.SYMBOL.value, "symbol_code_embedding.json"
    )

    DEFAULT_DOC_EMBEDDING_FPATH = os.path.join(
        get_config_fpath(), ConfigCategory.SYMBOL.value, "symbol_doc_embedding_l3.json"
    )

    # Used to cache the symbol subgraph across multiple instances
    _class_cache: Dict[str, Any] = {}

    def __init__(self, **kwargs) -> None:
        """
        Keyword Args (Defaults):
            symbol_graph_path (DependencyFactory.DEFAULT_SCIP_FPATH)
            flow_rank ("bidirectional")
            embedding_provider (OpenAIEmbedding())
            code_embedding_fpath (DependencyFactory.DEFAULT_CODE_EMBEDDING_FPATH)
            doc_embedding_fpath (DependencyFactory.DEFAULT_DOC_EMBEDDING_FPATH)
            symbol_rank_config (SymbolRankConfig())
            py_context_retriever_config (PyContextRetrieverConfig())
            coding_project_path (get_root_py_fpath())
            doc_completion_provider (OpenAIChatCompletionProvider())
        }
        """
        self._instances: Dict[str, Any] = {}
        self.overrides = kwargs

    def get(self, dependency: str) -> Any:
        """
        Gets a dependency by name.

        Raises:
            AgentGeneralError: If the dependency is not found

        Notes:
            Dependencies correspond to the method names of the DependencyFactory class.
            E.g. symbol_graph corresponds to `create_symbol_graph`.
        """
        if dependency in self.overrides:
            return self.overrides[dependency]

        if dependency in self._instances:
            return self._instances[dependency]

        method_name = f"create_{dependency}"
        if hasattr(self, method_name):
            creation_method = getattr(self, method_name)
            logger.info(f"Creating dependency {dependency}")
            instance = creation_method()
        else:
            raise AgentGeneralError(f"Dependency {dependency} not found.")

        self._instances[dependency] = instance

        return instance

    @classmethod_lru_cache()
    def create_symbol_graph(self) -> SymbolGraph:
        """
        Associated Keyword Args:
            symbol_graph_path (DependencyFactory.DEFAULT_SCIP_FPATH)
        """
        return SymbolGraph(
            self.overrides.get("symbol_graph_path", DependencyFactory.DEFAULT_SCIP_FPATH)
        )

    @classmethod_lru_cache()
    def create_subgraph(self) -> SymbolGraph.SubGraph:
        """
        Associated Keyword Args:
            flow_rank ("bidirectional")
        """
        symbol_graph = self.get("symbol_graph")
        return symbol_graph.get_rankable_symbol_dependency_subgraph(
            self.overrides.get("flow_rank", "bidirectional")
        )

    @classmethod_lru_cache()
    def create_symbol_code_similarity(self) -> SymbolSimilarityCalculator:
        """
        Associated Keyword Args:
            code_embedding_fpath (DependencyFactory.DEFAULT_CODE_EMBEDDING_FPATH)
            embedding_provider (OpenAIEmbedding())
        """
        code_embedding_fpath = self.overrides.get(
            "code_embedding_fpath", DependencyFactory.DEFAULT_CODE_EMBEDDING_FPATH
        )
        code_embedding_db = JSONVectorDatabase(code_embedding_fpath)

        embedding_provider = self.overrides.get("embedding_provider", OpenAIEmbeddingProvider())
        code_embedding_handler = SymbolCodeEmbeddingHandler(code_embedding_db, embedding_provider)
        return SymbolSimilarityCalculator(code_embedding_handler)

    @classmethod_lru_cache()
    def create_symbol_doc_similarity(self) -> SymbolSimilarityCalculator:
        """
        Associated Keyword Args:
            doc_embedding_fpath (DependencyFactory.DEFAULT_DOC_EMBEDDING_FPATH)
            embedding_provider (OpenAIEmbedding())
        """
        doc_embedding_fpath = self.overrides.get(
            "doc_embedding_fpath", DependencyFactory.DEFAULT_DOC_EMBEDDING_FPATH
        )
        doc_embedding_db = JSONVectorDatabase(doc_embedding_fpath)

        embedding_provider = self.overrides.get("embedding_provider", OpenAIEmbeddingProvider())
        symbol_search = self.get("symbol_search")
        py_context_retriever = self.get("py_context_retriever")
        completion_provider = self.overrides.get(
            "doc_completion_provider", OpenAIChatCompletionProvider()
        )

        doc_embedding_handler = SymbolDocEmbeddingHandler(
            doc_embedding_db,
            embedding_provider,
            completion_provider,
            symbol_search,
            py_context_retriever,
        )
        return SymbolSimilarityCalculator(doc_embedding_handler)

    @classmethod_lru_cache()
    def create_symbol_search(self) -> SymbolSearch:
        """
        Associated Keyword Args:
            symbol_rank_config (SymbolRankConfig())
        """
        symbol_graph = self.get("symbol_graph")
        symbol_code_similarity = self.get("symbol_code_similarity")
        symbol_rank_config = self.overrides.get("symbol_rank_config", SymbolRankConfig())
        symbol_graph_subgraph = self.get("subgraph")
        return SymbolSearch(
            symbol_graph,
            symbol_code_similarity,
            symbol_rank_config,
            symbol_graph_subgraph,
        )

    @classmethod_lru_cache()
    def create_py_context_retriever(self) -> PyContextRetriever:
        """
        Associated Keyword Args:
            py_context_retriever_config (PyContextRetrieverConfig())
        """
        symbol_graph = self.get("symbol_graph")
        py_context_retriever_config = self.overrides.get(
            "py_context_retriever_config", PyContextRetrieverConfig()
        )
        return PyContextRetriever(symbol_graph, py_context_retriever_config)

    @classmethod_lru_cache()
    def create_py_reader(self) -> PyReader:
        return PyReader()

    @classmethod_lru_cache()
    def create_py_writer(self) -> PyWriter:
        return PyWriter(self.get("py_reader"))


class AgentToolFactory:
    """The AgentToolFactory class is responsible for creating tools from a given agent tool name."""

    TOOLKIT_TYPE_TO_ARGS: Dict[AgentToolProviders, List[Tuple[str, Any]]] = {
        AgentToolProviders.PY_READER: [("py_reader", PyReader)],
        AgentToolProviders.PY_WRITER: [("py_writer", PyWriter)],
        AgentToolProviders.SYMBOL_SEARCH: [("symbol_search", SymbolSearch)],
        AgentToolProviders.CONTEXT_ORACLE: [
            ("symbol_search", SymbolSearch),
            ("symbol_doc_similarity", SymbolSimilarityCalculator),
        ],
    }

    @staticmethod
    def create_tools_from_builder(agent_tool: AgentToolProviders, **kwargs) -> Sequence[Tool]:
        """Uses the Builder Registry to create tools from a given agent tool name."""
        for builder in AutomataOpenAIAgentToolBuilderRegistry.get_all_builders():
            if builder.can_handle(agent_tool):
                if builder.PLATFORM == LLMProvider.OPENAI:
                    return builder(**kwargs).build_for_open_ai()
                else:
                    return builder(**kwargs).build()

        raise UnknownToolError(agent_tool.value)

    @staticmethod
    def build_tools(tool_list: List[str], **kwargs) -> List[Tool]:
        """Given a list of tools this method builds the tools and returns them."""
        tools: List[Tool] = []

        for tool_name in tool_list:
            tool_name = tool_name.strip()
            agent_tool_manager = AgentToolProviders(tool_name)

            if agent_tool_manager is None:
                raise UnknownToolError(agent_tool_manager)

            tools.extend(AgentToolFactory.create_tools_from_builder(agent_tool_manager, **kwargs))

        return tools
