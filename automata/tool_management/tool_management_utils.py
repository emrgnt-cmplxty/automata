import importlib
import logging
from typing import Dict, List, Optional

from automata.configs.automata_agent_configs import AutomataAgentConfig
from automata.core.base.tool import Tool, Toolkit, ToolkitType
from automata.core.utils import root_py_path
from automata.tool_management.base_tool_manager import BaseToolManager
from automata.tools.documentation.documentation_gpt import DocumentationGPT
from automata.tools.oracle.codebase_oracle import CodebaseOracle
from automata.tools.python_tools.python_indexer import PythonIndexer
from automata.tools.python_tools.python_writer import PythonWriter

logger = logging.getLogger(__name__)


class ToolManagerFactory:
    @staticmethod
    def create_tool_manager(toolkit_type: ToolkitType, inputs: dict) -> Optional[BaseToolManager]:
        model = inputs.get("model") or "gpt-4"
        documentation_url = inputs.get("documentation_url")
        temperature = inputs.get("temperature") or 0.7

        if toolkit_type == ToolkitType.PYTHON_INDEXER:
            python_indexer = PythonIndexer(root_py_path())
            PythonIndexerToolManager = importlib.import_module(
                "automata.tool_management.python_indexer_tool_manager"
            ).PythonIndexerToolManager
            return PythonIndexerToolManager(python_indexer=python_indexer)
        elif toolkit_type == ToolkitType.PYTHON_WRITER:
            python_indexer = PythonIndexer(root_py_path())
            PythonWriterToolManager = importlib.import_module(
                "automata.tool_management.python_writer_tool_manager"
            ).PythonWriterToolManager
            return PythonWriterToolManager(python_writer=PythonWriter(python_indexer))
        elif toolkit_type == ToolkitType.CODEBASE_ORACLE:
            CodebaseOracleToolManager = importlib.import_module(
                "automata.tool_management.codebase_oracle_tool_manager"
            ).CodebaseOracleToolManager
            return CodebaseOracleToolManager(
                codebase_oracle=CodebaseOracle.get_default_codebase_oracle()
            )
        elif toolkit_type == ToolkitType.DOCUMENTATION_GPT:
            DocumentationGPTToolManager = importlib.import_module(
                "automata.tool_management.documentation_gpt_tool_manager"
            ).DocumentationGPTToolManager
            return DocumentationGPTToolManager(
                documentation_gpt=DocumentationGPT(
                    url=documentation_url, model=model, temperature=temperature, verbose=True
                )
            )
        elif toolkit_type == ToolkitType.AUTOMATA_INDEXER:
            python_indexer = PythonIndexer(root_py_path())
            PythonIndexerToolManager = importlib.import_module(
                "automata.tool_management.python_indexer_tool_manager"
            ).PythonIndexerToolManager
            return PythonIndexerToolManager(python_indexer=python_indexer)
        elif toolkit_type == ToolkitType.AUTOMATA_WRITER:
            python_indexer = PythonIndexer(root_py_path())
            python_writer = PythonWriter(python_indexer)
            PythonWriterToolManager = importlib.import_module(
                "automata.tool_management.python_writer_tool_manager"
            ).PythonWriterToolManager
            return PythonWriterToolManager(python_writer=python_writer)
        else:
            return None


class ToolkitBuilder:
    def __init__(self, **kwargs):
        """Initializes a ToolkitBuilder object with the given inputs."""

        self.inputs = kwargs
        self._tool_management: Dict[ToolkitType, BaseToolManager] = {}

    def _build_toolkit(
        self, toolkit_type: ToolkitType, config: Optional[AutomataAgentConfig]
    ) -> Toolkit:
        """Builds a toolkit of the given type."""
        tool_manager = ToolManagerFactory.create_tool_manager(toolkit_type, self.inputs)

        if not tool_manager:
            raise ValueError("Unknown toolkit type: %s" % toolkit_type)

        if (
            toolkit_type == ToolkitType.AUTOMATA_WRITER
            or toolkit_type == ToolkitType.AUTOMATA_INDEXER
        ):
            assert config is not None, "Config must be provided for automata toolkits."
            tools = ToolkitBuilder.build_tools_with_automata(tool_manager, config)
        else:
            tools = ToolkitBuilder.build_tools(tool_manager)
        return Toolkit(tools)

    @staticmethod
    def build_tools(tool_manager: BaseToolManager) -> List[Tool]:
        """Build tools from a tool manager."""
        return tool_manager.build_tools()

    @staticmethod
    def build_tools_with_automata(
        tool_manager: BaseToolManager, config: AutomataAgentConfig
    ) -> List[Tool]:
        """Build tools from a tool manager with automata."""
        return tool_manager.build_tools_with_automata(config)


def build_llm_toolkits(tool_list: List[str], **kwargs) -> Dict[ToolkitType, Toolkit]:
    """
    Loads the tools specified in the tool_list and returns a dictionary of the loaded tools.

    Args:
        tool_list: A list of tool names to load.
        kwargs: A dictionary of inputs to pass to the tools.

    Returns:
        A dictionary of loaded tools.

    Raises:
        ValueError: If an unknown tool is specified.
    """

    toolkits: Dict[ToolkitType, Toolkit] = {}
    toolkit_builder = ToolkitBuilder(**kwargs)
    for tool_name in tool_list:
        tool_name = tool_name.strip()
        toolkit_type = None
        config = None
        if tool_name == "python_indexer":
            toolkit_type = ToolkitType.PYTHON_INDEXER
        elif tool_name == "python_writer":
            toolkit_type = ToolkitType.PYTHON_WRITER
        elif tool_name == "codebase_oracle":
            toolkit_type = ToolkitType.CODEBASE_ORACLE
        elif tool_name == "documentation_gpt":
            toolkit_type = ToolkitType.DOCUMENTATION_GPT
        elif tool_name == "automata_writer":
            toolkit_type = ToolkitType.AUTOMATA_WRITER
            config = kwargs.get("automata_writer_config")
        elif tool_name == "automata_indexer":
            toolkit_type = ToolkitType.AUTOMATA_INDEXER
            config = kwargs.get("automata_indexer_config")
        else:
            logger.warning("Unknown tool: %s", tool_name)
            raise ValueError(f"Unknown tool: {tool_name}")
        if not toolkit_type:
            raise ValueError(f"Unknown tool: {tool_name}")

        toolkit = toolkit_builder._build_toolkit(toolkit_type, config)  # type: ignore
        toolkits[toolkit_type] = toolkit

    return toolkits
