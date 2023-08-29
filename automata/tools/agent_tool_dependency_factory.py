from typing import Dict, List, Set, Any
from automata.tools.agent_tool_factory import AgentToolFactory
from automata.agent.agent import AgentToolkitNames
from automata.tools.agent_tool_dependency_factory import DependencyFactory
import logging
import logging.config
from automata.core.utils import get_logging_config

logger = logging.getLogger(__name__)
logging.config.dictConfig(get_logging_config())


def build_dependencies_for_tools(toolkits: List[str]) -> Dict[str, Any]:
    """Builds and returns a dictionary of all dependencies required by the given list of tools."""

    # Get an instance of the DependencyFactory
    dependency_factory = DependencyFactory()

    # Identify all unique dependencies
    dependencies: Set[str] = set()
    for tool_name in toolkits:
        tool_name = tool_name.strip()
        agent_tool = AgentToolkitNames(tool_name)

        # If tool_name is not in the mapping, raise an exception
        if agent_tool not in AgentToolFactory.TOOLKIT_TYPE_TO_ARGS:
            raise ValueError(f"Unknown tool: {tool_name}")

        dependencies.update([dep for dep, _ in AgentToolFactory.TOOLKIT_TYPE_TO_ARGS[agent_tool]])

    # Build dependencies
    tool_dependencies = {}
    logger.info(f"Building dependencies for toolkits {toolkits}...")
    for dependency in dependencies:
        logger.info(f"Building {dependency}...")
        tool_dependencies[dependency] = dependency_factory.get(dependency)

    return tool_dependencies
