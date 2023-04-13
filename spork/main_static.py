#!/usr/bin/env python3
import argparse
import sys
from typing import TextIO, cast

from langchain.agents import load_tools
from langchain.chat_models import ChatOpenAI

from .config import *  # noqa: F401, F403
from .tools.agent import AgentManager
from .tools.github import requests_get_clean
from .tools.python_tools import (
    PythonParser,
    PythonParserToolBuilder,
    PythonWriter,
    PythonWriterToolBuilder,
)
from .tools.utils import PassThroughBuffer

# Create argument parser and define arguments
parser = argparse.ArgumentParser(description="Modify main.py script to use passed-in args")
parser.add_argument("--planner_model", default="gpt-4", help="Planner model (default: gpt-4)")
parser.add_argument("--exec_model", default="gpt-3.5-turbo", help="Planner model (default: gpt-4)")
parser.add_argument(
    "--base_tools",
    default="",
    help="Base tools (default: " ", available: python_repl,terminal,human)",
)
parser.add_argument(
    "--load_request_tools",
    default=False,
    help="Load request tools? (default: False)",
)
parser.add_argument(
    "--load_python_tools",
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

pass_through_buffer = PassThroughBuffer(sys.stdout)
assert pass_through_buffer.saved_output == ""
sys.stdout = cast(TextIO, pass_through_buffer)
print("Loading Base Tools :%s" % (args.base_tools.split(",")))

planning_llm = ChatOpenAI(temperature=0, model=args.planner_model)
exec_llm = ChatOpenAI(temperature=0, model=args.exec_model)
base_tools = (
    load_tools(args.base_tools.split(","), llm=planning_llm) if args.base_tools != "" else []
)

if args.load_request_tools:
    print("Loading Request Tools")
    base_tools += [requests_get_clean]

exec_tools = base_tools

if args.load_python_tools:
    python_parser = PythonParser()
    exec_tools += PythonParserToolBuilder(python_parser).build_tools()
    python_writer = PythonWriter(python_parser)
    exec_tools += PythonWriterToolBuilder(python_writer).build_tools()


agent_manager = AgentManager(base_tools, planning_llm, exec_tools, exec_llm)

if args.do_plan:
    approved = False
    planning_task = agent_manager.make_planning_task()
    while not approved:
        instructions = agent_manager.plan_agent.run(planning_task)
        feedback = input(
            "Do you approve? If approved, type 'y'. If not approved, type why so the agent can try again: "
        )
        approved = feedback == "y"
        planning_task = feedback


# if args.do_plan:
#     plan_task = make_planning_task(exec_tools)
#     print("Planning task:", plan_task)
#     approved = False
#     while not approved:
#         instructions = plan_agent.run(plan_task)
#         print("Created new Instructions:", instructions)
#         feedback = input(
#             "Do you approve? If approved, type 'y'. If not approved, type why so the agent can try again: "
#         )
#         approved = feedback == "y"
#         plan_task = feedback

# # ask user if they want to run exec agent
# do_exec = input("Do you want to run the EXECUTION agent? (y/n)")
# if do_exec == "y":
#     exec_task = make_execution_task(work_item, instructions, github_repo.name)
#     print("Execution task:", exec_task)
#     try:
#         exec_agent.run(exec_task)
#     except ValueError as e:
#         if DO_RETRY:
#             tb = traceback.format_exc()
#             exec_task += f" This is your second attempt. During the previous attempt, you crashed with the following sequence: <run>{pass_through_buffer.saved_output}</run> Let's try again, avoiding previous mistakes."
#             pass_through_buffer.saved_output = ""
#             print(f"Failed to complete execution task with {e}")
#             print("New task:", exec_task)
#             print("Retrying...")
#             exec_agent.run(exec_task)
#     finally:
#         sys.stdout = pass_through_buffer.original_buffer
#         pygit_repo.git.checkout(args.branch_name)
