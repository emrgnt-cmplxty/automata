import logging
from typing import Any, List, Set

from automata.config import GITHUB_API_KEY, REPOSITORY_NAME
from automata.config.agent_config_builder import AutomataAgentConfigBuilder
from automata.config.config_types import AgentConfigName
from automata.core.agent.agent import AutomataOpenAIAgent
from automata.core.agent.tool.tool_utils import (
    AgentToolFactory,
    DependencyFactory,
    get_tool_builders,
)
from automata.core.base.github_manager import GitHubManager
from automata.core.base.tool import ToolkitType
from automata.core.coding.py.module_loader import py_module_loader

logger = logging.getLogger(__name__)

DEFAULT_ISSUES_PROMPT = """Provide an explanation and code snippets (in Markdown) which address the Github issue(s) that follow. You may use the context oracle (multiple times if necessary) to ensure that you have proper context to answer this question. Solve the GitHub issues by writing the relevant code via the PyWriter tool. The issues begin now:"""


def process_issues(issue_numbers: List[int], github_manager: GitHubManager) -> List[str]:
    """
    Process the issues and create tasks for each of them.

    Args:
        issue_numbers: The issue numbers to process.
    """
    issue_infos = []
    for issue_number in issue_numbers:
        issue = github_manager.fetch_issue(issue_number)
        if not issue:
            raise ValueError(f"Could not fetch issue #{issue_number}.")

        issue_info = f"Issue #{issue.number}: {issue.title}\n{issue.body}"
        issue_infos.append(issue_info)

    if not issue_infos:
        raise ValueError("No valid issues provided.")

    return issue_infos


def main(*args, **kwargs):
    py_module_loader.initialize()
    github_manager = GitHubManager(access_token=GITHUB_API_KEY, remote_name=REPOSITORY_NAME)

    # Pre-process issues if they are passsed
    issue_numbers = kwargs.get("fetch_issues", "")
    issue_numbers = list(map(int, issue_numbers.split(","))) if issue_numbers else []
    if len(issue_numbers):
        issue_infos = process_issues(issue_numbers, github_manager)
        # Concatenate instructions and issue information
        kwargs["instructions"] = kwargs.get("instructions") or DEFAULT_ISSUES_PROMPT + "\n".join(
            issue_infos
        )

    instructions = kwargs.get("instructions") or "This is a dummy instruction, return True."
    llm_toolkits_list = kwargs.get("tool_builders", "context_oracle").split(",")

    # A list of all dependencies that will be used to build the toolkits
    dependencies: Set[Any] = set()
    for tool in llm_toolkits_list:
        for dependency_name, _ in AgentToolFactory.TOOLKIT_TYPE_TO_ARGS[ToolkitType(tool)]:
            dependencies.add(dependency_name)

    print("dependencies = ", dependencies)
    # @### leave this commented out !@!@@
    # kwargs = {}

    # logger.info("  - Building dependencies...")
    # for dependency in dependencies:
    #     logger.info(f"Building {dependency}...")
    #     kwargs[dependency] = DependencyFactory().get(dependency)

    # tool_builders = build_llm_toolkits(llm_toolkits_list, **kwargs)
    # logger.info("Done building toolkits...")
    # @### leave this commented out !@!@@

    # config_name = AgentConfigName(kwargs.get("agent_name", "automata_reader"))
    # agent_config = (
    #     AutomataAgentConfigBuilder.from_name(config_name)
    #     .with_llm_toolkits(tool_builders)
    #     .with_model(kwargs.get("model", "gpt-4"))
    #     .build()
    # )

    # agent = AutomataOpenAIAgent(instructions, config=agent_config)
    # agent.setup()
    # return agent.run()
