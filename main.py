#!/usr/bin/env python3
from git import Repo
from langchain import OpenAI
from langchain.agents import initialize_agent, load_tools, AgentType
from langchain.chat_models import ChatOpenAI
from config import *

from custom_tools import GitToolBuilder
from utils import login_github, choose_issue, list_issues, list_repositories

# Log into GitHub
print("Logging into github")
github = login_github(GITHUB_API_KEY)

# List repositories

repositories = list_repositories(github)
print("Found repositories:", repositories)
# Let user choose a repository
repository_name = input("Enter the name of the repository you want to work with:")

github_repo = github.get_repo(repository_name)

# List issues in the repository
issues = list_issues(github_repo)

# Let user choose an issue
issue = choose_issue(issues)

# create a repo object which represents the repository we are inside of
pygit_repo = Repo(os.getcwd())

# reset to default branch if necessary
if pygit_repo.active_branch.name != "main":
    pygit_repo.git.checkout("main")

# checkout default branch and pull
pygit_repo.git.checkout("main")
pygit_repo.git.pull()

llm = ChatOpenAI(temperature=0, model="gpt-4")
# llm1 = OpenAI(temperature=0)
tools = load_tools(["python_repl", "terminal", "serpapi", "requests_get"], llm=llm)
tools += GitToolBuilder(github_repo, pygit_repo, issue).build_tools()


exec_agent = initialize_agent(
    tools, llm, agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)

task = (
    f"You are an AI software engineer. You contribute clean, high-quality code to the given codebase to close issues."
    f" You are working in {os.getcwd()} on {github_repo.name} repository."
    f" You may need to create, modify, or delete one or more files in this repository."
    f" You must create a new branch, implement a solution and submit a pull request to address the following issue: {issue.title}.\n\n {issue.body}."
    f" Don't use nano, vim or other text editors, but rather modify files directly either via python or terminal."
)
try:
    exec_agent.run(task)
except ValueError as e:
    if DO_RETRY:
        task += f" This is your second attempt. During the previous attempt, you crashed with the following error: {e}. Let's try again."
        exec_agent.run(task)
finally:
    pygit_repo.git.checkout("main")


