#!/usr/bin/env python3
import argparse
import os
import sys
import traceback
from typing import TextIO, cast

from git import Repo
from langchain.agents import AgentType, initialize_agent, load_tools
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory

from .config import DO_RETRY, GITHUB_API_KEY, PLANNER_AGENT_OUTPUT_STRING
from .tools.github import GithubToolBuilder, requests_get_clean
from .tools.prompts import make_execution_task, make_planning_task
from .tools.python_tools import PythonParser, PythonParserToolBuilder
from .tools.utils import PassThroughBuffer, choose_work_item, list_repositories, login_github

# Create argument parser and define arguments
parser = argparse.ArgumentParser(description="Modify main.py script to use passed-in args")
parser.add_argument("--branch_name", default="main", help="Default branch name (default: main)")
parser.add_argument(
    "--repository_name",
    default="maks-ivanov/improved-spork",
    help="Default branch name (default: main)",
)
parser.add_argument("--planner_model", default="gpt-4", help="Planner model (default: gpt-4)")
parser.add_argument(
    "--base_tools",
    default="python_repl,human",
    help="Base tools (default: python_repl,terminal,human)",
)
parser.add_argument(
    "--load_github_tools",
    default=True,
    help="Load github tools? (default: True)",
)
parser.add_argument(
    "--load_code_tools",
    default=True,
    help="Load code tools? (default: True)",
)
parser.add_argument(
    "--do_plan",
    default=True,
    help="Run the planning agent? (default: True)",
)
parser.add_argument(
    "--issues_or_prs",
    default="issues",
    help='Work on issues or pull requests? (default: "issues", alternative: "pulls")',
)


args = parser.parse_args()


# Log into GitHub
print("Logging into github")
github_client = login_github(GITHUB_API_KEY)

# List repositories

repositories = list_repositories(github_client)
print("Found recent repos:", repositories)
github_repo = github_client.get_repo(args.repository_name)


# create a repo PythonObjectType which represents the repository we are inside of
pygit_repo = Repo(os.getcwd())

# reset to default branch if necessary
if pygit_repo.active_branch.name != args.branch_name:
    pygit_repo.git.checkout(args.branch_name)


work_item = choose_work_item(github_repo, args.issues_or_prs)


llm = ChatOpenAI(temperature=0, model=args.planner_model)
# llm1 = OpenAI(temperature=0)
pass_through_buffer = PassThroughBuffer(sys.stdout)
assert pass_through_buffer.saved_output == ""
sys.stdout = cast(TextIO, pass_through_buffer)
print("Loading Base Tools :%s" % (args.base_tools.split(",")))
base_tools = load_tools(args.base_tools.split(","), llm=llm)
base_tools += [requests_get_clean]

exec_tools = base_tools
if args.load_github_tools:
    exec_tools += GithubToolBuilder(github_repo, pygit_repo, work_item).build_tools()

if args.load_code_tools:
    code_parser = PythonParser()
    exec_tools += PythonParserToolBuilder(code_parser).build_tools()

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

plan_agent = initialize_agent(
    base_tools,
    llm,
    agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
    verbose=True,
    memory=memory,
)

exec_agent = initialize_agent(
    exec_tools, llm, agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)

# check if instrutions are already attached to the issue
instructions_list = [
    c.body for c in work_item.get_comments() if c.body.startswith(PLANNER_AGENT_OUTPUT_STRING)
]
instructions = ""
if instructions_list:
    instructions = instructions_list.pop()
    instructions.replace(PLANNER_AGENT_OUTPUT_STRING, "")
    print("Found instructions:", instructions)

# ask user if they want to run planner agent, default is yes if no instructions

if args.do_plan:
    plan_task = make_planning_task(work_item, exec_tools, github_repo.name)
    print("Planning task:", plan_task)
    approved = False
    while not approved:
        instructions = plan_agent.run(plan_task)
        print("Created new Instructions:", instructions)
        feedback = input(
            "Do you approve? If approved, type 'y'. If not approved, type why so the agent can try again: "
        )
        approved = feedback == "y"
        plan_task = feedback

    # save instructions to issue
    work_item.create_comment(PLANNER_AGENT_OUTPUT_STRING + instructions)


# ask user if they want to run exec agent
do_exec = input("Do you want to run the EXECUTION agent? (y/n)")
if do_exec == "y":
    exec_task = make_execution_task(work_item, instructions, github_repo.name)
    print("Execution task:", exec_task)
    try:
        exec_agent.run(exec_task)
    except ValueError as e:
        if DO_RETRY:
            tb = traceback.format_exc()
            exec_task += f" This is your second attempt. During the previous attempt, you crashed with the following sequence: <run>{pass_through_buffer.saved_output}</run> Let's try again, avoiding previous mistakes."
            pass_through_buffer.saved_output = ""
            print(f"Failed to complete execution task with {e}")
            print("New task:", exec_task)
            print("Retrying...")
            exec_agent.run(exec_task)
    finally:
        sys.stdout = pass_through_buffer.original_buffer
        pygit_repo.git.checkout(args.branch_name)
