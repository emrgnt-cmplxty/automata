#!/usr/bin/env python3
import os
import sys
import traceback
from typing import TextIO, cast

from git import Repo
from langchain.agents import AgentType, initialize_agent, load_tools
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory, ReadOnlySharedMemory

from spork.tools.git_tools import GitToolBuilder, requests_get_clean
from spork.utils import PassThroughBuffer, choose_work_item, list_repositories, login_github

from .agents.text_editor_agent import make_text_editor_agent
from .config import DO_RETRY, GITHUB_API_KEY, PLANNER_AGENT_OUTPUT_STRING
from .prompts import make_execution_task, make_planning_task

# Log into GitHub
from .tools.codebase_oracle_tool import CodebaseOracleToolBuilder
from .tools.navigator_tool import LocalNavigatorTool
from .tools.text_editor_tool import TextEditorTool

print("Logging into github")
github_client = login_github(GITHUB_API_KEY)

# List repositories

repositories = list_repositories(github_client)
print("Found recent repos:", repositories)
# Let user choose a repository
repository_name = input("Enter the name of the repository you want to work with:")

github_repo = github_client.get_repo(repository_name)


# create a repo object which represents the repository we are inside of
pygit_repo = Repo(os.getcwd())

default_branch_name = "feature/text-editor-tool"
# reset to default branch if necessary
if pygit_repo.active_branch.name != default_branch_name:
    pygit_repo.git.checkout(default_branch_name)


work_item = choose_work_item(github_repo)


llm1 = ChatOpenAI(streaming=True, temperature=0, model="gpt-4")
llm2 = ChatOpenAI(streaming=True, temperature=0, model="gpt-4")

pass_through_buffer = PassThroughBuffer(sys.stdout)
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
readonlymemory = ReadOnlySharedMemory(memory=memory)
assert pass_through_buffer.saved_output == ""
sys.stdout = cast(TextIO, pass_through_buffer)
base_tools = load_tools(["python_repl", "human", "serpapi"], llm=llm2)
base_tools += [requests_get_clean]
exec_tools = base_tools + GitToolBuilder(github_repo, pygit_repo, work_item).build_tools()

exec_tools += [LocalNavigatorTool(llm2)]
codebase_oracle_builder = CodebaseOracleToolBuilder(os.getcwd(), llm2, readonlymemory)
codebase_oracle_tool = codebase_oracle_builder.build()

text_editor_agent = make_text_editor_agent(llm2, readonlymemory, os.getcwd())
text_editor_tool = TextEditorTool(text_editor_agent)

# planning_tools += [requests_get_clean]
# planning_tools = load_tools(["terminal"], llm=llm2)
breakpoint()
planning_tools = [codebase_oracle_tool]

exec_tools += planning_tools
plan_agent = initialize_agent(
    planning_tools,
    llm1,
    agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
    verbose=True,
    memory=memory,
)

exec_agent = initialize_agent(
    exec_tools, llm1, agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION, verbose=True
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

do_plan = input("Do you want to run the PLANNING agent? (y/n)")

if do_plan == "y":
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
            print(f"Failed to complete execution task with {e}, traceback: {tb}")
            print("New task:", exec_task)
            print("Retrying...")
            exec_task += f" This is your second attempt. During the previous attempt, you crashed with the following sequence: <run>{pass_through_buffer.saved_output}</run> Let's try again, avoiding previous mistakes."
            pass_through_buffer.saved_output = ""
            exec_agent.run(exec_task)
    finally:
        sys.stdout = pass_through_buffer.original_buffer
        pygit_repo.git.checkout(default_branch_name)
