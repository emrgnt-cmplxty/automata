#!/usr/bin/env python3
import sys
import traceback

from git import Repo
from github.Issue import Issue
from github.PullRequest import PullRequest
from langchain.agents import initialize_agent, load_tools, AgentType
from langchain.chat_models import ChatOpenAI

from config import *
from custom_tools import GitToolBuilder
from utils import login_github, list_repositories, choose_work_item, PassThroughBuffer

# Log into GitHub
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

# reset to default branch if necessary
if pygit_repo.active_branch.name != "main":
    pygit_repo.git.checkout("main")

# checkout default branch and pull
pygit_repo.git.checkout("main")
pygit_repo.git.pull()

work_item = choose_work_item(github_repo)


llm = ChatOpenAI(temperature=0.01, model="gpt-4")
# llm1 = OpenAI(temperature=0)
pass_through_buffer = PassThroughBuffer(sys.stdout)
assert pass_through_buffer.saved_output == ""
sys.stdout = pass_through_buffer
tools = load_tools(["python_repl", "terminal", "serpapi", "requests_get"], llm=llm)
tools += GitToolBuilder(github_repo, pygit_repo, work_item).build_tools()

exec_agent = initialize_agent(
    tools, llm, agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)


task = (
    f"You are a GPT-4-powered software engineer agent."
    f" You are built with langchain, a framework for building language-based agents. "
    f" You can read about it here: https://python.langchain.com/en/latest/modules/agents.html"
    f" Your task is to contribute clean, high-quality code to the given codebase."
    f" You are working in {os.getcwd()} on {github_repo.name} repository."
    f" Feel free to look around this repo. You can browse the internet for documentation and examples."
    f" You may need to create, modify, or delete one or more files in this repository."
)

if type(work_item) == Issue:
    task += f" You must create a new branch, implement a solution and submit a pull request to address the following issue: \n\n Title: {work_item.title}.\n\n Body: {work_item.body}."
if type(work_item) == PullRequest:
    task += (
        f" You must checkout the branch, understand the following pull request feedback make a commit with changes to address it:"
        f" \n\n Title: {work_item.title}.\n\n Body: {work_item.body}. \n\n Files: {[f.filename for f in work_item.get_files()]}:"
    )


comments = work_item.get_comments()

if list(comments):
    task += f" Comments:"
    for comment in comments:
        task += f" {comment.body}"


task += (
    f"\n\nUseful tips: Don't use nano, vim or other text editors, but rather modify files directly either via python or terminal. "
    f" Before creating a new branch, make sure to pick a name that is not taken."
)

try:
    print("Task:", task)
    x = exec_agent.run(task)
except ValueError as e:
    if DO_RETRY:
        tb = traceback.format_exc()
        task += f" This is your second attempt. During the previous attempt, you crashed with the following sequence: <run>{pass_through_buffer.saved_output}</run> Let's try again, avoiding previous mistakes."
        pass_through_buffer.saved_output = ""
        print("Failed to complete task with following error:", e, tb)
        print("New task:", task)
        print("Retrying...")
        x = exec_agent.run(task)
finally:
    sys.stdout = pass_through_buffer.original_buffer
    pygit_repo.git.checkout("main")
