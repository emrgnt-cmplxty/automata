#!/usr/bin/env python3
from git import Repo
from langchain.agents import initialize_agent, load_tools, AgentType
from langchain.llms import OpenAIChat

from config import *

# Use GPT-3 model
from custom_tools import GitToolBuilder
from utils import login_github, choose_issue, list_issues, list_repositories

# Main loop
task_id_counter = 1
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


llm = OpenAIChat(temperature=0, model="gpt-3.5-turbo")
tools = load_tools(["python_repl", "terminal", "serpapi"], llm=llm)
tools += GitToolBuilder(github_repo, pygit_repo, issue).build_tools()


exec_agent = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)

task = (
    f"You are an AI software engineer. You contribute clean, high-quality code to the given codebase to close issues. "
    f" You are working in {os.getcwd()} on {github_repo.name} repository."
    f" You must create a new branch, implement a solution and submit a pull request to address the following issue: {issue.title}.\n\n {issue.body}."
    f" Don't use nano or other text editors, but rather modify directly"
)
exec_agent.run(task)
