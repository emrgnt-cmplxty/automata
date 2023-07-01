import logging
import os
from functools import lru_cache
from typing import Any, Dict, List, Sequence, Set, Tuple

from automata.config.base import ConfigCategory, LLMProvider
from automata.core.agent.error import AgentGeneralError, UnknownToolError
from automata.core.base.agent import AgentToolkitNames
from automata.core.base.singleton import Singleton
from automata.core.base.symbol_embedding import JSONSymbolEmbeddingVectorDatabase
from automata.core.base.tool import Tool
from automata.core.coding.py.reader import PyReader
from automata.core.coding.py.writer import PyWriter
from automata.core.context.py.retriever import (
    PyContextRetriever,
    PyContextRetrieverConfig,
)
from automata.core.llm.providers.openai import (
    OpenAIChatCompletionProvider,
    OpenAIEmbeddingProvider,
)
from automata.core.memory_store.symbol_code_embedding import SymbolCodeEmbeddingHandler
from automata.core.memory_store.symbol_doc_embedding import SymbolDocEmbeddingHandler
from automata.core.symbol.graph import SymbolGraph
from automata.core.symbol.search.rank import SymbolRank, SymbolRankConfig
from automata.core.symbol.search.symbol_search import SymbolSearch
from automata.core.symbol_embedding.builders import SymbolDocEmbeddingBuilder
from automata.core.symbol_embedding.similarity import SymbolSimilarityCalculator
from automata.core.utils import get_config_fpath

logger = logging.getLogger(__name__)


class DependencyFactory(metaclass=Singleton):
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
    _class_cache: Dict[Tuple[str, ...], Any] = {}

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
        The dependency argument corresponds to the names of the creation methods of the DependencyFactory class
        without the 'create_' prefix. For example, to get a SymbolGraph instance you'd call `get('symbol_graph')`.

        Args:
            dependency (str): The name of the dependency to be retrieved.

        Returns:
            The instance of the requested dependency.

        Raises:
            AgentGeneralError: If the dependency is not found.

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

    def build_dependencies_for_tools(self, toolkit_list: List[str]) -> Dict[str, Any]:
        """Builds and returns a dictionary of all dependencies required by the given list of tools."""
        # Identify all unique dependencies
        dependencies: Set[str] = set()
        for tool_name in toolkit_list:
            tool_name = tool_name.strip()
            agent_tool = AgentToolkitNames(tool_name)

            if agent_tool is None:
                raise UnknownToolError(agent_tool)

            for dependency_name, _ in AgentToolFactory.TOOLKIT_TYPE_TO_ARGS[agent_tool]:
                dependencies.add(dependency_name)

        # Build dependencies
        tool_dependencies = {}
        logger.info(f"Building dependencies for toolkit_list {toolkit_list}...")
        for dependency in dependencies:
            logger.info(f"Building {dependency}...")
            tool_dependencies[dependency] = self.get(dependency)

        return tool_dependencies

    @lru_cache()
    def create_symbol_graph(self) -> SymbolGraph:
        """
        Associated Keyword Args:
            symbol_graph_path (DependencyFactory.DEFAULT_SCIP_FPATH)
        """
        return SymbolGraph(
            self.overrides.get("symbol_graph_path", DependencyFactory.DEFAULT_SCIP_FPATH)
        )

    @lru_cache()
    def create_subgraph(self) -> SymbolGraph.SubGraph:
        """
        Associated Keyword Args:
            flow_rank ("bidirectional")
        """
        symbol_graph = self.get("symbol_graph")
        return symbol_graph.get_rankable_symbol_dependency_subgraph(
            self.overrides.get("flow_rank", "bidirectional")
        )

    @lru_cache()
    def create_symbol_code_similarity(self) -> SymbolSimilarityCalculator:
        """
        Associated Keyword Args:
            code_embedding_fpath (DependencyFactory.DEFAULT_CODE_EMBEDDING_FPATH)
            embedding_provider (OpenAIEmbedding())
        """
        code_embedding_fpath = self.overrides.get(
            "code_embedding_fpath", DependencyFactory.DEFAULT_CODE_EMBEDDING_FPATH
        )
        code_embedding_db = JSONSymbolEmbeddingVectorDatabase(code_embedding_fpath)

        embedding_provider = self.overrides.get("embedding_provider", OpenAIEmbeddingProvider())
        code_embedding_handler = SymbolCodeEmbeddingHandler(code_embedding_db, embedding_provider)
        return SymbolSimilarityCalculator(code_embedding_handler, embedding_provider)

    @lru_cache()
    def create_symbol_doc_similarity(self) -> SymbolSimilarityCalculator:
        """
        Associated Keyword Args:
            doc_embedding_fpath (DependencyFactory.DEFAULT_DOC_EMBEDDING_FPATH)
            embedding_provider (OpenAIEmbedding())
        """
        doc_embedding_fpath = self.overrides.get(
            "doc_embedding_fpath", DependencyFactory.DEFAULT_DOC_EMBEDDING_FPATH
        )
        doc_embedding_db = JSONSymbolEmbeddingVectorDatabase(doc_embedding_fpath)

        embedding_provider = self.overrides.get("embedding_provider", OpenAIEmbeddingProvider())
        symbol_search = self.get("symbol_search")
        py_context_retriever = self.get("py_context_retriever")
        completion_provider = self.overrides.get(
            "doc_completion_provider", OpenAIChatCompletionProvider()
        )

        symbol_doc_embedding_builder = SymbolDocEmbeddingBuilder(
            embedding_provider, completion_provider, symbol_search, py_context_retriever
        )
        doc_embedding_handler = SymbolDocEmbeddingHandler(
            doc_embedding_db, symbol_doc_embedding_builder
        )
        return SymbolSimilarityCalculator(doc_embedding_handler, embedding_provider)

    @lru_cache()
    def create_symbol_rank(self) -> SymbolRank:
        """
        Associated Keyword Args:
            symbol_rank_config (SymbolRankConfig())
        """
        subgraph = self.get("subgraph")
        return SymbolRank(
            subgraph.graph, self.overrides.get("symbol_rank_config", SymbolRankConfig())
        )

    @lru_cache()
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

    @lru_cache()
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

    @lru_cache()
    def create_py_reader(self) -> PyReader:
        return PyReader()

    @lru_cache()
    def create_py_writer(self) -> PyWriter:
        return PyWriter(self.get("py_reader"))


class AgentToolFactory:
    """The AgentToolFactory class is responsible for creating tools from a given agent tool name."""

    TOOLKIT_TYPE_TO_ARGS: Dict[AgentToolkitNames, List[Tuple[str, Any]]] = {
        AgentToolkitNames.PY_READER: [("py_reader", PyReader)],
        AgentToolkitNames.PY_WRITER: [("py_writer", PyWriter)],
        AgentToolkitNames.SYMBOL_SEARCH: [("symbol_search", SymbolSearch)],
        AgentToolkitNames.CONTEXT_ORACLE: [
            ("symbol_doc_similarity", SymbolSimilarityCalculator),
            ("symbol_code_similarity", SymbolSimilarityCalculator),
        ],
    }

    @staticmethod
    def create_tools_from_builder(agent_tool: AgentToolkitNames, **kwargs) -> Sequence[Tool]:
        """Uses the Builder Registry to create tools from a given agent tool name."""
        from automata.core.agent.tool.registry import (  # import here for easy mocking
            AutomataOpenAIAgentToolkitRegistry,
        )

        for builder in AutomataOpenAIAgentToolkitRegistry.get_all_builders():
            if builder.can_handle(agent_tool):
                if builder.PLATFORM == LLMProvider.OPENAI:
                    return builder(**kwargs).build_for_open_ai()
                else:
                    return builder(**kwargs).build()

        raise UnknownToolError(agent_tool.value)

    @staticmethod
    def build_tools(toolkit_list: List[str], **kwargs) -> List[Tool]:
        """Given a list of tools this method builds the tools and returns them."""
        tools: List[Tool] = []

        for tool_name in toolkit_list:
            tool_name = tool_name.strip()
            agent_tool_manager = AgentToolkitNames(tool_name)

            if agent_tool_manager is None:
                raise UnknownToolError(agent_tool_manager)

            tools.extend(AgentToolFactory.create_tools_from_builder(agent_tool_manager, **kwargs))

        return tools


dependency_factory = DependencyFactory()
