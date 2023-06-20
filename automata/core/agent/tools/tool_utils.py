import logging
import os
from typing import Any, Dict, List, Tuple

from automata.config.config_types import ConfigCategory
from automata.core.agent.tools.agent_tool import AgentTool
from automata.core.agent.tools.context_oracle import ContextOracleTool
from automata.core.agent.tools.py_code_retriever import PyCodeRetrieverTool
from automata.core.agent.tools.py_code_writer import PyCodeWriterTool
from automata.core.agent.tools.symbol_search import SymbolSearchTool
from automata.core.base.tool import Tool, Toolkit, ToolkitType
from automata.core.coding.py_coding.retriever import PyCodeRetriever
from automata.core.coding.py_coding.writer import PyCodeWriter
from automata.core.context.py_context.retriever import (
    PyContextRetriever,
    PyContextRetrieverConfig,
)
from automata.core.database.vector import JSONVectorDatabase
from automata.core.embedding.code_embedding import SymbolCodeEmbeddingHandler
from automata.core.embedding.doc_embedding import SymbolDocEmbeddingHandler
from automata.core.embedding.embedding_types import OpenAIEmbedding
from automata.core.embedding.symbol_similarity import SymbolSimilarity
from automata.core.symbol.graph import SymbolGraph
from automata.core.symbol.search.rank import SymbolRankConfig
from automata.core.symbol.search.symbol_search import SymbolSearch
from automata.core.utils import config_fpath

logger = logging.getLogger(__name__)


class DependencyFactory:
    """Creates dependencies for input Toolkit construction."""

    DEFAULT_SCIP_FPATH = os.path.join(config_fpath(), ConfigCategory.SYMBOL.value, "index.scip")

    DEFAULT_CODE_EMBEDDING_FPATH = os.path.join(
        config_fpath(), ConfigCategory.SYMBOL.value, "symbol_code_embedding.json"
    )

    DEFAULT_DOC_EMBEDDING_FPATH = os.path.join(
        config_fpath(), ConfigCategory.SYMBOL.value, "symbol_doc_embedding_l3.json"
    )

    def __init__(self, **kwargs) -> None:
        """
        Acceptable Overrides (kwargs):
            symbol_graph_path - Defaults to DependencyFactory.DEFAULT_SCIP_FPATH
            flow_rank - Defaults to "bidirectional"
            embedding_provider - Defaults to OpenAIEmbedding()
            code_embedding_fpath - Defaults to DependencyFactory.DEFAULT_CODE_EMBEDDING_FPATH
            doc_embedding_fpath - Defaults to DependencyFactory.DEFAULT_DOC_EMBEDDING_FPATH
            symbol_rank_config - Defaults to SymbolRankConfig()
            py_context_retriever_config - Defaults to PyContextRetrieverConfig()
        }
        """
        self._instances: Dict[str, Any] = {}
        self.overrides = kwargs

    def get(self, dependency: str) -> Any:
        if dependency in self.overrides:
            return self.overrides[dependency]

        if dependency in self._instances:
            return self._instances[dependency]

        method_name = f"create_{dependency}"
        if hasattr(self, method_name):
            creation_method = getattr(self, method_name)
            logger.info("Creating dependency {dependency}")
            instance = creation_method()
        else:
            raise ValueError(f"Dependency {dependency} not found.")

        self._instances[dependency] = instance

        return instance

    def create_symbol_graph(self) -> SymbolGraph:
        return SymbolGraph(
            self.overrides.get("symbol_graph_path", DependencyFactory.DEFAULT_SCIP_FPATH)
        )

    def create_subgraph(self) -> SymbolGraph.SubGraph:
        symbol_graph = self.get("symbol_graph")
        return symbol_graph.get_rankable_symbol_subgraph(
            self.overrides.get("flow_rank", "bidirectional")
        )

    def create_symbol_code_similarity(self) -> SymbolSimilarity:
        code_embedding_fpath = self.overrides.get(
            "code_embedding_fpath", DependencyFactory.DEFAULT_CODE_EMBEDDING_FPATH
        )
        code_embedding_db = JSONVectorDatabase(code_embedding_fpath)

        embedding_provider = self.overrides.get("embedding_provider", OpenAIEmbedding())
        code_embedding_handler = SymbolCodeEmbeddingHandler(code_embedding_db, embedding_provider)
        return SymbolSimilarity(code_embedding_handler)

    def create_symbol_doc_similarity(self) -> SymbolSimilarity:
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

    def create_symbol_search(self) -> SymbolSearch:
        symbol_graph = self.get("symbol_graph")
        symbol_code_similarity = self.get("symbol_code_similarity")
        symbol_rank_config = self.overrides.get("symbol_rank_config", SymbolRankConfig())
        symbol_graph_subgraph = self.get("subgraph")
        return SymbolSearch(
            symbol_graph, symbol_code_similarity, symbol_rank_config, symbol_graph_subgraph
        )

    def create_py_context_retriever(self) -> PyContextRetriever:
        symbol_graph = self.get("symbol_graph")
        py_context_retriever_config = self.overrides.get(
            "py_context_retriever_config", PyContextRetrieverConfig()
        )
        return PyContextRetriever(symbol_graph, py_context_retriever_config)


class ToolCreationError(Exception):
    """An exception for when a tool cannot be created."""

    ERROR_STRING = "Must provide a valid %s to construct a %s."

    def __init__(self, arg_type: str, class_name: str) -> None:
        super().__init__(self.ERROR_STRING % (arg_type, class_name))


class UnknownToolError(Exception):
    """An exception for when an unknown toolkit type is provided."""

    ERROR_STRING = "Unknown toolkit type: %s"

    def __init__(self, tool_kit: ToolkitType) -> None:
        super().__init__(self.ERROR_STRING % (tool_kit))


class AgentToolFactory:
    """
    A class for creating tool managers.
    TODO: It is unfortunate that we must maintain these mappings locally
        in this class. It would be better if we could generate it dynamically
        perhaps by using a decorator on the tool classes themselves.
    """

    _retriever_instance = None

    TOOLKIT_TYPE_TO_TOOL_CLASS = {
        ToolkitType.PY_RETRIEVER: PyCodeRetrieverTool,
        ToolkitType.PY_WRITER: PyCodeWriterTool,
        ToolkitType.SYMBOL_SEARCHER: SymbolSearchTool,
        ToolkitType.CONTEXT_ORACLE: ContextOracleTool,
    }

    TOOLKIT_TYPE_TO_ARGS: Dict[ToolkitType, List[Tuple[str, Any]]] = {
        ToolkitType.PY_RETRIEVER: [("py_retriever", PyCodeRetriever)],
        ToolkitType.PY_WRITER: [("py_writer", PyCodeWriter)],
        ToolkitType.SYMBOL_SEARCHER: [("symbol_search", SymbolSearch)],
        ToolkitType.CONTEXT_ORACLE: [
            ("symbol_search", SymbolSearch),
            ("symbol_doc_similarity", SymbolSimilarity),
        ],
    }

    @staticmethod
    def create_agent_tool(toolkit_type: ToolkitType, **kwargs) -> AgentTool:
        """
        Create a tool manager for the specified toolkit type.

        Args:
            toolkit_type (ToolkitType): The type of toolkit to create a tool manager for.

            kwargs (Additional Args): Additional arguments, which should contain the required AgentTool arguments
              for the specified toolkit type. The possible arguments are:
                py_retriever - PyCodeRetriever
                py_writer - PyCodeWriter
                symbol_search - SymbolSearch
                symbol_doc_similarity - SymbolSimilarity

        Returns:
            AgentTool: The tool manager for the specified toolkit type.

        Raises:
            ToolCreationError: If the required arguments are not provided.
            UnknownToolError: If the toolkit type is not recognized.
        """

        if toolkit_type not in AgentToolFactory.TOOLKIT_TYPE_TO_TOOL_CLASS:
            raise UnknownToolError(toolkit_type)

        tool_class = AgentToolFactory.TOOLKIT_TYPE_TO_TOOL_CLASS[toolkit_type]
        args = AgentToolFactory.TOOLKIT_TYPE_TO_ARGS[toolkit_type]

        tool_kwargs = {}
        for arg_name, arg_class in args:
            arg_value = kwargs.get(arg_name, None)
            if arg_value is None or not isinstance(arg_value, arg_class):
                raise ToolCreationError(arg_name, tool_class.__name__)
            tool_kwargs[arg_name] = arg_value

        return tool_class(**tool_kwargs)


class ToolkitBuilder:
    """A class for building toolkits."""

    def __init__(self, **kwargs) -> None:
        """
        Initializes a ToolkitBuilder.

        Note:
            The kwargs should contain the required AgentTool arguments for the specified toolkit type.
            For more information, see the AgentToolFactory.create_agent_tool method.
        """

        self._tool_management: Dict[ToolkitType, AgentTool] = {}
        self.kwargs = kwargs

    def build_toolkit(self, toolkit_type: ToolkitType) -> Toolkit:
        """
        Builds a toolkit of the given type.

        Args:
            toolkit_type (ToolkitType): The type of toolkit to build.

        Returns:
            Toolkit: The toolkit of the given type.

        Raises:
            UnknownToolError: If the toolkit type is not recognized.
        """
        agent_tool = AgentToolFactory.create_agent_tool(toolkit_type, **self.kwargs)

        if not agent_tool:
            raise UnknownToolError(toolkit_type)

        tools = ToolkitBuilder.build(agent_tool)
        return Toolkit(tools)

    @staticmethod
    def build(agent_tool: AgentTool) -> List[Tool]:
        """
        Build tools from a tool manager.

        Args:
            agent_tool (AgentTool): The agent tool to build.

        Returns:
            List[Tool]: The list of tools built from the tool manager.
        """
        return agent_tool.build()


def build_llm_toolkits(tool_list: List[str], **kwargs) -> Dict[ToolkitType, Toolkit]:
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
    toolkits: Dict[ToolkitType, Toolkit] = {}
    toolkit_builder = ToolkitBuilder(**kwargs)

    for tool_name in tool_list:
        tool_name = tool_name.strip()
        toolkit_type = ToolkitType(tool_name)

        if toolkit_type is None:
            raise UnknownToolError(toolkit_type)

        toolkit = toolkit_builder.build_toolkit(toolkit_type)
        toolkits[toolkit_type] = toolkit

    return toolkits
