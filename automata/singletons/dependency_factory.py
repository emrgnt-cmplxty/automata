import os
from functools import lru_cache
from typing import Any, Dict, List, Set, Tuple

import networkx as nx

from automata.agent.agent import AgentToolkitNames
from automata.agent.error import AgentGeneralError, UnknownToolError
from automata.code_handling.py.reader import PyReader
from automata.code_handling.py.writer import PyWriter
from automata.config.base import ConfigCategory
from automata.context_providers.symbol_synchronization import (
    SymbolProviderSynchronizationContext,
)
from automata.core.base.patterns.singleton import Singleton
from automata.core.utils import get_config_fpath
from automata.embedding.base import EmbeddingSimilarityCalculator
from automata.experimental.search.rank import SymbolRank, SymbolRankConfig
from automata.experimental.search.symbol_search import SymbolSearch
from automata.llm.providers.openai import (
    OpenAIChatCompletionProvider,
    OpenAIEmbeddingProvider,
)
from automata.memory_store.symbol_code_embedding import SymbolCodeEmbeddingHandler
from automata.memory_store.symbol_doc_embedding import SymbolDocEmbeddingHandler
from automata.retrievers.py.context import PyContextRetriever, PyContextRetrieverConfig
from automata.symbol.base import ISymbolProvider
from automata.symbol.graph import SymbolGraph
from automata.symbol_embedding.base import JSONSymbolEmbeddingVectorDatabase
from automata.symbol_embedding.builders import (
    SymbolCodeEmbeddingBuilder,
    SymbolDocEmbeddingBuilder,
)
from automata.tools.factory import AgentToolFactory, logger


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
            disable_synchronization (False): Disable synchronization of ISymbolProvider dependencies and created classes?
            symbol_graph_scip_fpath (DependencyFactory.DEFAULT_SCIP_FPATH): Filepath to the SCIP index file.
            code_embedding_fpath (DependencyFactory.DEFAULT_CODE_EMBEDDING_FPATH): Filepath to the code embedding database.
            doc_embedding_fpath (DependencyFactory.DEFAULT_DOC_EMBEDDING_FPATH): Filepath to the doc embedding database.
            coding_project_path (get_root_py_fpath()): Filepath to the root of the coding project.
            symbol_rank_config (SymbolRankConfig()): Configuration for the SymbolRank algorithm.
            py_context_retriever_config (PyContextRetrieverConfig()): Configuration for the PyContextRetriever.
            embedding_provider (OpenAIEmbedding()): The embedding provider to use.
            llm_completion_provider (OpenAIChatCompletionProvider()): The LLM completion provider to use.
            py_retriever_doc_embedding_db (None): The doc embedding database to use for the PyContextRetriever.
        }
        """
        self._instances: Dict[str, Any] = {}
        self.overrides = kwargs

    def set_overrides(self, **kwargs) -> None:
        if self._class_cache:
            raise AgentGeneralError("Cannot set overrides after dependencies have been created.")

        for override_obj in kwargs.values():
            if isinstance(override_obj, ISymbolProvider):
                self._synchronize_provider(override_obj)

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

        # Perform synchronization
        if isinstance(instance, ISymbolProvider):
            self._synchronize_provider(instance)

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

    def _synchronize_provider(self, provider: ISymbolProvider) -> None:
        """Synchronize an ISymbolProvider instance."""
        if not self.overrides.get("disable_synchronization", False):
            with SymbolProviderSynchronizationContext() as synchronization_context:
                synchronization_context.register_provider(provider)
                synchronization_context.synchronize()

    @lru_cache()
    def create_symbol_graph(self) -> SymbolGraph:
        """
        Associated Keyword Args:
            symbol_graph_scip_fpath (DependencyFactory.DEFAULT_SCIP_FPATH)
        """
        return SymbolGraph(
            self.overrides.get("symbol_graph_scip_fpath", DependencyFactory.DEFAULT_SCIP_FPATH)
        )

    @lru_cache()
    def create_subgraph(self) -> nx.DiGraph:
        symbol_graph: SymbolGraph = self.get("symbol_graph")
        return symbol_graph.default_rankable_subgraph

    @lru_cache()
    def create_symbol_rank(self) -> SymbolRank:
        """
        Associated Keyword Args:
            symbol_rank_config (SymbolRankConfig())
        """
        subgraph: nx.DiGraph = self.get("subgraph")
        return SymbolRank(subgraph, self.overrides.get("symbol_rank_config", SymbolRankConfig()))

    @lru_cache()
    def create_symbol_code_embedding_handler(self) -> SymbolCodeEmbeddingHandler:
        """
        Associated Keyword Args:
            code_embedding_fpath (DependencyFactory.DEFAULT_CODE_EMBEDDING_FPATH)
            embedding_provider (OpenAIEmbedding())
        """
        code_embedding_db = JSONSymbolEmbeddingVectorDatabase(
            self.overrides.get(
                "code_embedding_fpath", DependencyFactory.DEFAULT_CODE_EMBEDDING_FPATH
            )
        )
        embedding_provider: OpenAIEmbeddingProvider = self.overrides.get(
            "embedding_provider", OpenAIEmbeddingProvider()
        )
        embedding_builder: SymbolCodeEmbeddingBuilder = SymbolCodeEmbeddingBuilder(
            embedding_provider
        )

        return SymbolCodeEmbeddingHandler(code_embedding_db, embedding_builder)

    @lru_cache()
    def create_symbol_doc_embedding_handler(self) -> SymbolDocEmbeddingHandler:
        """
        Associated Keyword Args:
            doc_embedding_fpath (DependencyFactory.DEFAULT_CODE_EMBEDDING_FPATH)
            embedding_provider (OpenAIEmbedding())
        """

        doc_embedding_db = JSONSymbolEmbeddingVectorDatabase(
            self.overrides.get(
                "doc_embedding_fpath", DependencyFactory.DEFAULT_DOC_EMBEDDING_FPATH
            )
        )
        embedding_provider: OpenAIEmbeddingProvider = self.overrides.get(
            "embedding_provider", OpenAIEmbeddingProvider()
        )
        llm_completion_provider: OpenAIChatCompletionProvider = self.overrides.get(
            "llm_completion_provider", OpenAIChatCompletionProvider()
        )
        symbol_search: SymbolSearch = self.get("symbol_search")
        retriver: PyContextRetriever = self.get("py_context_retriever")

        embedding_builder = SymbolDocEmbeddingBuilder(
            embedding_provider, llm_completion_provider, symbol_search, retriver
        )

        return SymbolDocEmbeddingHandler(doc_embedding_db, embedding_builder)

    @lru_cache()
    def create_symbol_search(self) -> SymbolSearch:
        """
        Associated Keyword Args:
            symbol_rank_config (SymbolRankConfig())
        """
        symbol_graph: SymbolGraph = self.get("symbol_graph")
        symbol_rank_config: SymbolRankConfig = self.overrides.get(
            "symbol_rank_config", SymbolRankConfig()
        )
        symbol_code_embedding_handler: SymbolCodeEmbeddingBuilder = self.get(
            "symbol_code_embedding_handler"
        )
        embedding_similarity_calculator: EmbeddingSimilarityCalculator = self.get(
            "embedding_similarity_calculator"
        )
        return SymbolSearch(
            symbol_graph,
            symbol_rank_config,
            # FIXME - Fix this type ignore
            symbol_code_embedding_handler,  # type: ignore
            embedding_similarity_calculator,
        )

    @lru_cache()
    def create_py_context_retriever(self) -> PyContextRetriever:
        """
        Associated Keyword Args:
            py_context_retriever_config (PyContextRetrieverConfig())
            py_retriever_doc_embedding_db (None)
        """
        symbol_graph: SymbolGraph = self.get("symbol_graph")
        py_context_retriever_config: PyContextRetrieverConfig = self.overrides.get(
            "py_context_retriever_config", PyContextRetrieverConfig()
        )
        return PyContextRetriever(
            symbol_graph,
            py_context_retriever_config,
            self.overrides.get("py_retriever_doc_embedding_db"),
        )

    @lru_cache()
    def create_embedding_similarity_calculator(self) -> EmbeddingSimilarityCalculator:
        """
        Associated Keyword Args:
            embedding_provider (OpenAIEmbedding())
        """
        embedding_provider: OpenAIEmbeddingProvider = self.overrides.get(
            "embedding_provider", OpenAIEmbeddingProvider()
        )
        return EmbeddingSimilarityCalculator(embedding_provider)

    @lru_cache()
    def create_py_reader(self) -> PyReader:
        return PyReader()

    @lru_cache()
    def create_py_writer(self) -> PyWriter:
        py_reader: PyReader = self.get("py_reader")
        return PyWriter(py_reader)


dependency_factory = DependencyFactory()
