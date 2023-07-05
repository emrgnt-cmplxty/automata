import logging
from typing import List

from automata.config import GITHUB_API_KEY, REPOSITORY_NAME
from automata.config.base import AgentConfigName
from automata.config.openai_agent import OpenAIAutomataAgentConfigBuilder
from automata.core.agent.providers import OpenAIAutomataAgent
from automata.core.github_management.client import GitHubClient
from automata.core.singletons.dependency_factory import dependency_factory
from automata.core.singletons.py_module_loader import py_module_loader
from automata.core.tools.factory import AgentToolFactory

logger = logging.getLogger(__name__)

DEFAULT_ISSUES_PROMPT_PREFIX = """Provide a comprehensive explanation and full code implementation (in Markdown) which address the Github issue(s) that follow:"""

DEFAULT_ISSUES_PROMPT_SUFFIX = """You may use the context oracle (multiple times if necessary) to ensure that you have proper context to answer this question. If you are tasked with writing code, then keep to the SOLID Principles Further, pay special attention to Dependency Inversion Principle and Dependency Injection."""
# Solve the GitHub issues by writing the relevant code via the PyWriter tool. The issues begin now:"""


def process_issues(issue_numbers: List[int], github_manager: GitHubClient) -> List[str]:
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
    github_manager = GitHubClient(access_token=GITHUB_API_KEY, remote_name=REPOSITORY_NAME)

    # Pre-process issues if they are passsed
    issue_numbers = kwargs.get("fetch_issues", "")
    issue_numbers = list(map(int, issue_numbers.split(","))) if issue_numbers else []
    if len(issue_numbers):
        issue_infos = process_issues(issue_numbers, github_manager)
        # Concatenate instructions and issue information
        kwargs["instructions"] = (
            kwargs.get("instructions")
            or DEFAULT_ISSUES_PROMPT_PREFIX + "\n".join(issue_infos) + DEFAULT_ISSUES_PROMPT_SUFFIX
        )

    instructions = kwargs.get("instructions") or "This is a dummy instruction, return True."
    toolkit_list = kwargs.get("toolkit_list", "context-oracle").split(",")

    tool_dependencies = dependency_factory.build_dependencies_for_tools(toolkit_list)
    tools = AgentToolFactory.build_tools(toolkit_list, **tool_dependencies)
    logger.info("Done building tools...")
    config_name = AgentConfigName(kwargs.get("agent_name", "automata-main"))
    agent_config = (
        OpenAIAutomataAgentConfigBuilder.from_name(config_name)
        .with_tools(tools)
        .with_model(kwargs.get("model", "gpt-4-0613"))
        .build()
    )

    agent = OpenAIAutomataAgent(instructions, config=agent_config)
    result = agent.run()
    print("Final result:\n\n", result)
    return result
