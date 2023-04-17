"""
task_generators.py - a module containing task generators for planning and execution agents.

This module contains two functions for generating planning and execution tasks for agents. These functions are:
- make_planning_task: A function for generating a planning task for an agent.
- make_execution_task: A function for generating an execution task for an agent.

Functions:
- make_planning_task: A function for generating a planning task for an agent.
- make_execution_task: A function for generating an execution task for an agent.
"""

import os
from typing import List, Union

from github.Issue import Issue
from github.PullRequest import PullRequest
from langchain.tools import BaseTool

from .config import PLANNER_AGENT_OUTPUT_STRING


def make_planning_task(
    work_item: Union[Issue, PullRequest],
    exec_tools: List[BaseTool],
    github_repo_name: str,
):
    """
    Generates a planning task for an agent.

    Args:
    - work_item (Union[Issue, PullRequest]): An object representing the work item to generate a planning task for.
    - exec_tools (List[BaseTool]): A list of tools that the execution agent has access to.
    - github_repo_name (str): The name of the GitHub repository the work item belongs to.

    Returns:
    - task_instructions (str): A string containing the instructions for the planning task.
    """
    pr_or_issue_str = (
        " submit a pull request" if isinstance(work_item, Issue) else " make a commit "
    )
    return (
        f"You are a GPT-4 a planner agent of a self-assembling codebase."
        f" You plan out software engineering work for developer agents."
        f" You are built with langchain, a framework for building language-based agents."
        f" Assume you have the code locally on your machine."  # todo
        f" You are working in {os.getcwd()} on {github_repo_name} repository."
        f" Your task is to thoroughly understand the following work item and "
        f" create simple and thorough step-by-step instructions for a developer to implement the solution."
        f" You should not make the changes yourself, but rather output instructions for a developer to make the changes."
        f" \n\nTitle: {work_item.title}"
        f" \n\nBody: {work_item.body}"
        f" \n\nComments: {[c.body for c in work_item.get_comments() if not c.body.startswith(PLANNER_AGENT_OUTPUT_STRING)]}"
        f" \n\n The developer will use your instructions to make changes to the repository and"
        f" {pr_or_issue_str} with working, clean, and documented code."
        f" Your developer is also a GPT-4-powered agent, so keep that in mind when creating instructions."
        f" You should ALWAYS start by asking clarifying questions using the oracles. "
        f" Make sure not to regress any existing functionality."
        f" The developer agent will have access to the following tools: {[(tool.name, tool.description) for tool in exec_tools]}, so keep that in mind when creating instructions."
        f" Begin."
    )


def make_execution_task(
    work_item: Union[Issue, PullRequest],
    solution_instructions: str,
    github_repo_name: str,
):
    """
    Generates an execution task for an agent.

    Args:
    - work_item (Union[Issue, PullRequest]): An object representing the work item to generate an execution task for.
    - solution_instructions (str): A string containing the solution instructions for the work item.
    - github_repo_name (str): The name of the GitHub repository the work item belongs to.

    Returns:
    - task_instructions (str): A string containing the instructions for the execution task.
    """

    pr_or_issue_str = (
        " create a pull request with your changes."
        if isinstance(work_item, Issue)
        else " make a commit with your changes to the appropriate branch."
    )
    return (
        f"You are a GPT-4-powered coding agent."
        f" You are built with langchain, a framework for building language-based agents. "
        f" You can read about it here: https://python.langchain.com/en/latest/modules/agents.html"
        f" Your task is to contribute clean, high-quality code to the given codebase."
        f" You are working in {os.getcwd()} on {github_repo_name} repository."
        f" Assume the repository is private, so don't try to look it up on the internet, but find it locally on your machine."
        f" You are working on the following work item: "
        f"\n\nTitle: {work_item.title};"
        f"\n\nBody: {work_item.body};"
        f"\n\nComments: {[c.body for c in work_item.get_comments() if not c.body.startswith(PLANNER_AGENT_OUTPUT_STRING)]};"
        f"\n\n A planning agent has created the following step-by-step instructions for you: <instructions>{solution_instructions}</instructions>"
        f" Execute the instructions thoroughly and"
        f" {pr_or_issue_str}"
        f" Some of the instructions may be high level, so it's up to you to understand what exactly needs to be done."
        f" Your code oracle tool is really powerful so use it to search for code and ask questions about it."
        f" If you run into any errors, be thoughtful about why they occurred and how to resolve them."
        f" Make sure not to regress any existing functionality."
        f"\n\nUseful tips: when following git-create-branch instructions, make sure to use a branch name that's not taken. "
    )
