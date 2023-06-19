import logging
from typing import Any, Dict, List, Tuple

from automata.core.agent.tools.agent_tool import AgentTool
from automata.core.agent.tools.context_oracle import ContextOracleTool
from automata.core.agent.tools.py_code_retriever import PyCodeRetrieverTool
from automata.core.agent.tools.py_code_writer import PyCodeWriterTool
from automata.core.agent.tools.symbol_search import SymbolSearchTool
from automata.core.base.tool import Tool, Toolkit, ToolkitType
from automata.core.coding.py_coding.retriever import PyCodeRetriever
from automata.core.coding.py_coding.writer import PyCodeWriter
from automata.core.embedding.symbol_similarity import SymbolSimilarity
from automata.core.symbol.search.symbol_search import SymbolSearch

logger = logging.getLogger(__name__)


class ToolCreationError(Exception):
    """An exception for when a tool cannot be created."""

    ERROR_STRING = "Must provide a valid %s to construct a %s."

    def __init__(self, arg_type: str, class_name: str):
        super().__init__(self.ERROR_STRING % (arg_type, class_name))


class UnknownToolError(Exception):
    """An exception for when an unknown toolkit type is provided."""

    ERROR_STRING = "Unknown toolkit type: %s"

    def __init__(self, tool_kit: ToolkitType):
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

    def __init__(self, **kwargs):
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
