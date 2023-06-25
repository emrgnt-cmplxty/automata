import functools
import logging
import os
from typing import Any, Dict, List, Tuple

from automata.config.config_types import AvailableAgentTools, ConfigCategory
from automata.core.agent.tool.py_reader_builder import (
    PyReaderOpenAIToolBuilder,
    PyReaderToolBuilder,
)
from automata.core.agent.tool.registry import AgentToolManagerRegistry
from automata.core.agent.tools.agent_tool import AgentTool
from automata.core.base.agent import AgentToolBuilder
from automata.core.base.database.vector import JSONVectorDatabase
from automata.core.coding.py.reader import PyReader
from automata.core.coding.py.writer import PyWriter
from automata.core.context.py.retriever import (
    PyContextRetriever,
    PyContextRetrieverConfig,
)
from automata.core.embedding.code_embedding import SymbolCodeEmbeddingHandler
from automata.core.embedding.doc_embedding import SymbolDocEmbeddingHandler
from automata.core.embedding.symbol_similarity import SymbolSimilarity
from automata.core.llm.providers.openai import OpenAIEmbedding
from automata.core.symbol.graph import SymbolGraph
from automata.core.symbol.search.rank import SymbolRankConfig
from automata.core.symbol.search.symbol_search import SymbolSearch
from automata.core.utils import config_fpath

logger = logging.getLogger(__name__)


def classmethod_lru_cache():
    """
    Class method LRU cache decorator.

    Returns:
        decorator: A decorator that caches the return value of a class method
    """

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
    """Creates dependencies for input Toolkit construction."""

    DEFAULT_SCIP_FPATH = os.path.join(config_fpath(), ConfigCategory.SYMBOL.value, "index.scip")

    DEFAULT_CODE_EMBEDDING_FPATH = os.path.join(
        config_fpath(), ConfigCategory.SYMBOL.value, "symbol_code_embedding.json"
    )

    DEFAULT_DOC_EMBEDDING_FPATH = os.path.join(
        config_fpath(), ConfigCategory.SYMBOL.value, "symbol_doc_embedding_l3.json"
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
        }
        """
        self._instances: Dict[str, Any] = {}
        self.overrides = kwargs

    def get(self, dependency: str) -> Any:
        """
        Gets a dependency by name.

        Args:
            dependency: The name of the dependency to get

        Returns:
            The dependency instance

        Raises:
            ValueError: If the dependency is not found

        Notes:
            Dependencies correspond to the method names of the DependencyFactory class.
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
            raise ValueError(f"Dependency {dependency} not found.")

        self._instances[dependency] = instance

        return instance

    @classmethod_lru_cache()
    def create_symbol_graph(self) -> SymbolGraph:
        """
        Creates a SymbolGraph instance.

        Keyword Args:
            symbol_graph_path (DependencyFactory.DEFAULT_SCIP_FPATH)
        """
        return SymbolGraph(
            self.overrides.get("symbol_graph_path", DependencyFactory.DEFAULT_SCIP_FPATH)
        )

    @classmethod_lru_cache()
    def create_subgraph(self) -> SymbolGraph.SubGraph:
        """
        Creates a SymbolGraph.SubGraph instance.

        Keyword Args:
            flow_rank ("bidirectional")
        """
        symbol_graph = self.get("symbol_graph")
        return symbol_graph.get_rankable_symbol_subgraph(
            self.overrides.get("flow_rank", "bidirectional")
        )

    @classmethod_lru_cache()
    def create_symbol_code_similarity(self) -> SymbolSimilarity:
        """
        Creates a SymbolSimilarity instance for symbol code similarity.

        Keyword Args:
            code_embedding_fpath (DependencyFactory.DEFAULT_CODE_EMBEDDING_FPATH)
            embedding_provider (OpenAIEmbedding())
        """
        code_embedding_fpath = self.overrides.get(
            "code_embedding_fpath", DependencyFactory.DEFAULT_CODE_EMBEDDING_FPATH
        )
        code_embedding_db = JSONVectorDatabase(code_embedding_fpath)

        embedding_provider = self.overrides.get("embedding_provider", OpenAIEmbedding())
        code_embedding_handler = SymbolCodeEmbeddingHandler(code_embedding_db, embedding_provider)
        return SymbolSimilarity(code_embedding_handler)

    @classmethod_lru_cache()
    def create_symbol_doc_similarity(self) -> SymbolSimilarity:
        """
        Creates a SymbolSimilarity instance for symbol doc similarity.

        Keyword Args:
            doc_embedding_fpath (DependencyFactory.DEFAULT_DOC_EMBEDDING_FPATH)
            embedding_provider (OpenAIEmbedding())
        """
        doc_embedding_fpath = self.overrides.get(
            "doc_embedding_fpath", DependencyFactory.DEFAULT_DOC_EMBEDDING_FPATH
        )
        doc_embedding_db = JSONVectorDatabase(doc_embedding_fpath)

        embedding_provider = self.overrides.get("embedding_provider", OpenAIEmbedding())
        symbol_search = self.get("symbol_search")
        py_context_retriever = self.get("py_context_retriever")

        doc_embedding_handler = SymbolDocEmbeddingHandler(
            doc_embedding_db, embedding_provider, symbol_search, py_context_retriever
        )
        return SymbolSimilarity(doc_embedding_handler)

    @classmethod_lru_cache()
    def create_symbol_search(self) -> SymbolSearch:
        """
        Creates a SymbolSearch instance.

        Keyword Args:
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
        Creates a PyContextRetriever instance.

        Keyword Args:
            py_context_retriever_config (PyContextRetrieverConfig())
        """
        symbol_graph = self.get("symbol_graph")
        py_context_retriever_config = self.overrides.get(
            "py_context_retriever_config", PyContextRetrieverConfig()
        )
        return PyContextRetriever(symbol_graph, py_context_retriever_config)

    @classmethod_lru_cache()
    def create_py_reader(self) -> PyReader:
        """
        Creates a PyReader instance.
        """
        return PyReader()

    @classmethod_lru_cache()
    def create_py_writer(self) -> PyWriter:
        """
        Creates a PyReader instance.
        """
        return PyWriter(self.get("py_reader"))


class ToolCreationError(Exception):
    """An exception for when a tool cannot be created."""

    ERROR_STRING = "Must provide a valid %s to construct a %s."

    def __init__(self, arg_type: str, class_name: str) -> None:
        super().__init__(self.ERROR_STRING % (arg_type, class_name))


class UnknownToolError(Exception):
    """An exception for when an unknown toolkit type is provided."""

    ERROR_STRING = "Unknown toolkit type: %s"

    def __init__(self, tool_kit: AvailableAgentTools) -> None:
        super().__init__(self.ERROR_STRING % (tool_kit))


# class AgentToolManagerFactory:
#     """
#     A class for creating tool managers.
#     TODO: It is unfortunate that we must maintain these mappings locally
#         in this class. It would be better if we could generate it dynamically
#         perhaps by using a decorator on the tool classes themselves.
#     """

#     _retriever_instance = None

#     TOOLKIT_TYPE_TO_TOOL_CLASS = {
#         AgentToolManagers.PY_READER: PyReaderOpenAIToolManager,
#         # ToolkitType.PY_WRITER: PyWriterTool,
#         # ToolkitType.SYMBOL_SEARCH: SymbolSearchTool,
#         # ToolkitType.CONTEXT_ORACLE: ContextOracleTool,
#     }

#     TOOLKIT_TYPE_TO_ARGS: Dict[AgentToolManagers, List[Tuple[str, Any]]] = {
#         AgentToolManagers.PY_READER: [("py_reader", PyReader)],
#         # ToolkitType.PY_WRITER: [("py_writer", PyWriter)],
#         # ToolkitType.SYMBOL_SEARCH: [("symbol_search", SymbolSearch)],
#         # ToolkitType.CONTEXT_ORACLE: [
#         #     ("symbol_search", SymbolSearch),
#         #     ("symbol_doc_similarity", SymbolSimilarity),
#         # ],
#     }

#     @staticmethod
#     def create_agent_tool_manager(tool_manager: AgentToolManagers, **kwargs) -> AgentToolManager:
#         """
#         Create a tool manager for the specified toolkit type.

#         Args:
#             toolkit_type (ToolkitType): The type of toolkit to create a tool manager for.

#             kwargs (Additional Args): Additional arguments, which should contain the required AgentTool arguments
#               for the specified toolkit type. The possible arguments are:
#                 py_reader - PyReader
#                 py_writer - PyWriter
#                 symbol_search - SymbolSearch
#                 symbol_doc_similarity - SymbolSimilarity

#         Returns:
#             AgentTool: The tool manager for the specified toolkit type.

#         Raises:
#             ToolCreationError: If the required arguments are not provided.
#             UnknownToolError: If the toolkit type is not recognized.
#         """

#         if tool_manager not in AgentToolManagerFactory.TOOLKIT_TYPE_TO_TOOL_CLASS:
#             raise UnknownToolError(tool_manager)

#         tool_class = AgentToolManagerFactory.TOOLKIT_TYPE_TO_TOOL_CLASS[tool_manager]
#         args = AgentToolManagerFactory.TOOLKIT_TYPE_TO_ARGS[tool_manager]

#         tool_kwargs = {}
#         for arg_name, arg_class in args:
#             arg_value = kwargs.get(arg_name, None)
#             if arg_value is None or not isinstance(arg_value, arg_class):
#                 raise ToolCreationError(arg_name, tool_class.__name__)
#             tool_kwargs[arg_name] = arg_value
#         print("tool_kwargs = ", tool_kwargs)
#         print("creating tool...")
#         return tool_class(**tool_kwargs)


class AgentToolManagerFactory:
    TOOLKIT_TYPE_TO_ARGS: Dict[AvailableAgentTools, List[Tuple[str, Any]]] = {
        AvailableAgentTools.PY_READER: [("py_reader", PyReader)],
        # ToolkitType.PY_WRITER: [("py_writer", PyWriter)],
        # ToolkitType.SYMBOL_SEARCH: [("symbol_search", SymbolSearch)],
        # ToolkitType.CONTEXT_ORACLE: [
        #     ("symbol_search", SymbolSearch),
        #     ("symbol_doc_similarity", SymbolSimilarity),
        # ],
    }
    ALL_MANAGERS = []

    @staticmethod
    def register_tool_manager(cls):
        AgentToolManagerFactory.ALL_MANAGERS.append(cls)
        return cls

    @staticmethod
    def create_agent_tool_manager(tool_manager: AvailableAgentTools, **kwargs) -> AgentToolBuilder:
        for manager in AgentToolManagerRegistry.ALL_MANAGERS:
            if manager.can_handle(tool_manager):
                return manager(**kwargs)
        raise UnknownToolError(tool_manager)


def build_llm_tool_managers(
    tool_list: List[str], **kwargs
) -> Dict[AvailableAgentTools, AgentToolBuilder]:
    """
    This function builds a list of toolkits from a list of toolkit names.

    Args:
        tool_list (List[str]): A list of toolkit names.
          These tool names must map onto valid ToolkitType values.

    Returns:
        Dict[ToolkitType, Toolkit]: A dictionary mapping toolkit types to toolkits.

    Raises:
        UnknownToolError: If a toolkit name is not recognized.

    """
    tool_managers: Dict[AvailableAgentTools, AgentToolBuilder] = {}

    for tool_name in tool_list:
        tool_name = tool_name.strip()
        agent_tool_manager = AvailableAgentTools(tool_name)

        if agent_tool_manager is None:
            raise UnknownToolError(agent_tool_manager)

        # toolkit = toolkit_builder.build_toolkit(agent_tool_manager)
        tool_managers[agent_tool_manager] = AgentToolManagerFactory.create_agent_tool_manager(
            agent_tool_manager, **kwargs
        )

    return tool_managers
