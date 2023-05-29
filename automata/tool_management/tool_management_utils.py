import importlib
import logging
from typing import Dict, List

from automata.core.base.tool import Tool, Toolkit, ToolkitType
from automata.core.code_indexing.python_code_retriever import PythonCodeRetriever
from automata.core.search.symbol_factory import SymbolSearcherFactory
from automata.tool_management.base_tool_manager import BaseToolManager
from automata.tools.python_tools.python_writer import PythonWriter

logger = logging.getLogger(__name__)


class ToolManagerFactory:
    """
    A class for creating tool managers.
    """

    _retriever_instance = None  # store instance of PythonCodeRetriever

    @staticmethod
    def create_tool_manager(toolkit_type: ToolkitType) -> BaseToolManager:
        if toolkit_type == ToolkitType.PYTHON_RETRIEVER:
            if ToolManagerFactory._retriever_instance is None:
                ToolManagerFactory._retriever_instance = PythonCodeRetriever()

            PythonCodeRetrieverToolManager = importlib.import_module(
                "automata.tool_management.python_code_retriever_tool_manager"
            ).PythonCodeRetrieverToolManager
            return PythonCodeRetrieverToolManager(
                python_retriever=ToolManagerFactory._retriever_instance
            )
        elif toolkit_type == ToolkitType.PYTHON_WRITER:
            if ToolManagerFactory._retriever_instance is None:
                ToolManagerFactory._retriever_instance = PythonCodeRetriever()

            PythonWriterToolManager = importlib.import_module(
                "automata.tool_management.python_writer_tool_manager"
            ).PythonWriterToolManager
            return PythonWriterToolManager(
                python_writer=PythonWriter(ToolManagerFactory._retriever_instance)
            )
        elif toolkit_type == ToolkitType.COVERAGE_PROCESSOR:
            CoverageToolManager = importlib.import_module(
                "automata.tool_management.coverage_tool_manager"
            ).CoverageToolManager
            return CoverageToolManager()
        elif toolkit_type == ToolkitType.SYMBOL_SEARCHER:
            SymbolSearcherToolManager = importlib.import_module(
                "automata.tool_management.symbol_searcher_tool_manager"
            ).SymbolSearcherToolManager
            return SymbolSearcherToolManager(
                symbol_searcher=SymbolSearcherFactory().create(
                    index_name="index.scip", symbol_embedding_name="symbol_embedding.json"
                )
            )
        else:
            raise ValueError("Unknown toolkit type: %s" % toolkit_type)


class ToolkitBuilder:
    def __init__(self, **kwargs):
        """Initializes a ToolkitBuilder object with the given inputs."""

        self._tool_management: Dict[ToolkitType, BaseToolManager] = {}

    def _build_toolkit(self, toolkit_type: ToolkitType) -> Toolkit:
        """Builds a toolkit of the given type."""
        tool_manager = ToolManagerFactory.create_tool_manager(toolkit_type)

        if not tool_manager:
            raise ValueError("Unknown toolkit type: %s" % toolkit_type)
        tools = ToolkitBuilder.build_tools(tool_manager)
        return Toolkit(tools)

    @staticmethod
    def build_tools(tool_manager: BaseToolManager) -> List[Tool]:
        """Build tools from a tool manager."""
        return tool_manager.build_tools()


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
        elif tool_name == "coverage_processor":
            toolkit_type = ToolkitType.COVERAGE_PROCESSOR
        elif tool_name == "symbol_searcher":
            toolkit_type = ToolkitType.SYMBOL_SEARCHER
        else:
            logger.warning("Unknown tool: %s", tool_name)
            continue

        toolkit = toolkit_builder._build_toolkit(toolkit_type)  # type: ignore
        toolkits[toolkit_type] = toolkit

    return toolkits
