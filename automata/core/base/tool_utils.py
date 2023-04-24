import logging
from enum import Enum, auto
from typing import Dict, List, Optional

from automata.core.utils import root_py_path
from automata.tools.documentation_tools.documentation_gpt import DocumentationGPT
from automata.tools.oracle.codebase_oracle import CodebaseOracle
from automata.tools.python_tools.python_indexer import PythonIndexer
from automata.tools.python_tools.python_writer import PythonWriter
from automata.tools.tool_management import (
    CodebaseOracleToolManager,
    DocumentationGPTToolManager,
    PythonIndexerToolManager,
    PythonWriterToolManager,
    build_tools,
    build_tools_with_automata,
)
from automata.tools.tool_management.base_tool_manager import BaseToolManager

from .tool import Tool

logger = logging.getLogger(__name__)


class Toolkit:
    """A toolkit of tools."""

    def __init__(self, tools: List[Tool]):
        self.tools = tools

    def __repr__(self) -> str:
        return f"Toolkit(tools={self.tools})"


class ToolkitType(Enum):
    """An enum representing the different types of toolkits that can be built."""

    PYTHON_INDEXER = auto()
    PYTHON_WRITER = auto()
    CODEBASE_ORACLE = auto()
    DOCUMENTATION_GPT = auto()
    AUTOMATA_INDEXER = auto()
    AUTOMATA_WRITER = auto()
    MOCK_TOOLKIT = "mock_toolkit"


class ToolkitBuilder:
    def __init__(self, **kwargs):
        """Initializes a ToolkitBuilder object with the given inputs."""

        self.inputs = kwargs
        self._tool_management: Dict[ToolkitType, BaseToolManager] = {}

    def _build_toolkit(self, toolkit_type: ToolkitType) -> Optional[Toolkit]:
        """Builds a toolkit of the given type."""

        model = self.inputs.get("model") or "gpt-4"
        documentation_url = self.inputs.get("documentation_url")
        temperature = self.inputs.get("temperature") or 0.7

        tool_manager: Optional[BaseToolManager] = None
        if toolkit_type == ToolkitType.PYTHON_INDEXER:
            python_indexer = PythonIndexer(root_py_path())
            tool_manager = PythonIndexerToolManager(python_indexer=python_indexer)
        elif toolkit_type == ToolkitType.PYTHON_WRITER:
            python_indexer = PythonIndexer(root_py_path())
            tool_manager = PythonWriterToolManager(python_writer=PythonWriter(python_indexer))
        elif toolkit_type == ToolkitType.CODEBASE_ORACLE:
            tool_manager = CodebaseOracleToolManager(
                codebase_oracle=CodebaseOracle.get_default_codebase_oracle()
            )
        elif toolkit_type == ToolkitType.DOCUMENTATION_GPT:
            tool_manager = DocumentationGPTToolManager(
                documentation_gpt=DocumentationGPT(
                    url=documentation_url,
                    model=model,
                    temperature=temperature,
                    verbose=True,
                )
            )

        elif toolkit_type == ToolkitType.AUTOMATA_INDEXER:
            python_indexer = PythonIndexer(root_py_path())
            tool_manager = PythonIndexerToolManager(python_indexer=python_indexer)
        elif toolkit_type == ToolkitType.AUTOMATA_WRITER:
            python_indexer = PythonIndexer(root_py_path())
            python_writer = PythonWriter(python_indexer)
            tool_manager = PythonWriterToolManager(python_writer=python_writer)

        if not tool_manager:
            logger.warning("Unknown toolkit type: %s", toolkit_type)
            return None

        if (
            toolkit_type == ToolkitType.AUTOMATA_WRITER
            or toolkit_type == ToolkitType.AUTOMATA_INDEXER
        ):
            tools = build_tools_with_automata(tool_manager)
        else:
            tools = build_tools(tool_manager)
        return Toolkit(tools)


def load_llm_toolkits(tool_list: List[str], **kwargs) -> Dict[ToolkitType, Toolkit]:
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
        elif tool_name == "automata_indexer":
            toolkit_type = ToolkitType.AUTOMATA_INDEXER
        elif tool_name == "mock_toolkit":
            toolkit_type = ToolkitType.MOCK_TOOLKIT
        else:
            logger.warning("Unknown tool: %s", tool_name)
            raise ValueError(f"Unknown tool: {tool_name}")

        toolkit = toolkit_builder._build_toolkit(toolkit_type)
        if toolkit:
            toolkits[toolkit_type] = toolkit

    return toolkits
