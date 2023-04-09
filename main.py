#!/usr/bin/env python3
from git import Repo
from langchain.agents import initialize_agent, load_tools, AgentType
from langchain.chat_models import ChatOpenAI

from config import *
from custom_tools import GitToolBuilder
from utils import login_github, list_repositories, choose_work_item

# Log into GitHub
print("Logging into github")
github = login_github(GITHUB_API_KEY)

# List repositories

repositories = list_repositories(github)
print("Found repositories:", repositories)
# Let user choose a repository
repository_name = input("Enter the name of the repository you want to work with:")

github_repo = github.get_repo(repository_name)


# create a repo object which represents the repository we are inside of
pygit_repo = Repo(os.getcwd())

# reset to default branch if necessary
if pygit_repo.active_branch.name != "main":
    pygit_repo.git.checkout("main")

# checkout default branch and pull
pygit_repo.git.checkout("main")
pygit_repo.git.pull()

work_item = choose_work_item(github_repo)


llm = ChatOpenAI(temperature=0, model="gpt-4")
# llm1 = OpenAI(temperature=0)
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

if type(work_item) == github.Issue.Issue:
    task += f" You must create a new branch, implement a solution and submit a pull request to address the following issue: \n\n Title: {work_item.title}.\n\n Body: {work_item.body}."
if type(work_item) == github.PullRequest.PullRequest:
    task += (
        f" You must checkout the branch, understand the following pull request feedback make a commit with changes to address it:"
        f" \n\n Title: {work_item.title}.\n\n Body: {work_item.body}. \n\n Files: {[f.filename for f in work_item.get_files()]}:"
    )


comments = work_item.get_comments()

if comments:
    task += f" Comments:"
    for comment in comments:
        task += f" {comment.body}"


task += f" Don't use nano, vim or other text editors, but rather modify files directly either via python or terminal."


try:
    exec_agent.run(task)
except ValueError as e:
    if DO_RETRY:
        task += f" This is your second attempt. During the previous attempt, you crashed with the following error: {e}. Let's try again."
        exec_agent.run(task)
finally:
    pygit_repo.git.checkout("main")
