#!/usr/bin/env python3
import base64
import os
import sys
import time
from collections import deque
from typing import Dict, List

# !/usr/bin/env python3
import openai
import pinecone
from dotenv import load_dotenv
from github import Github
from git import Repo
from langchain.llms import OpenAI, OpenAIChat
from langchain.agents import initialize_agent, Tool, tool, load_tools, AgentType


# Set Variables
load_dotenv()

# Set API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
assert OPENAI_API_KEY, "OPENAI_API_KEY environment variable is missing from .env"

GITHUB_API_KEY = os.getenv("GITHUB_API_KEY", "")
assert GITHUB_API_KEY, "GITHUB_API_KEY environment variable is missing from .env"

# Use GPT-3 model
USE_GPT4 = False
if USE_GPT4:
    print("\033[91m\033[1m" + "\n*****USING GPT-4. POTENTIALLY EXPENSIVE. MONITOR YOUR COSTS*****" + "\033[0m\033[0m")

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY", "")
assert PINECONE_API_KEY, "PINECONE_API_KEY environment variable is missing from .env"

PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT", "us-east1-gcp")
assert PINECONE_ENVIRONMENT, "PINECONE_ENVIRONMENT environment variable is missing from .env"

# Table config
YOUR_TABLE_NAME = os.getenv("TABLE_NAME", "")
assert YOUR_TABLE_NAME, "TABLE_NAME environment variable is missing from .env"

# Project config
OBJECTIVE = sys.argv[1] if len(sys.argv) > 1 else os.getenv("OBJECTIVE", "")
# assert OBJECTIVE, "OBJECTIVE environment variable is missing from .env"

# YOUR_FIRST_TASK = os.getenv("FIRST_TASK", "")
# assert YOUR_FIRST_TASK, "FIRST_TASK environment variable is missing from .env"

# Print OBJECTIVE
print("\033[96m\033[1m" + "\n*****OBJECTIVE*****\n" + "\033[0m\033[0m")
print(OBJECTIVE)

# Configure OpenAI and Pinecone
openai.api_key = OPENAI_API_KEY
pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENVIRONMENT)

# Create Pinecone index
table_name = YOUR_TABLE_NAME
dimension = 1536
metric = "cosine"
pod_type = "p1"
if table_name not in pinecone.list_indexes():
    pinecone.create_index(table_name, dimension=dimension, metric=metric, pod_type=pod_type)

# Connect to the index
index = pinecone.Index(table_name)

# Task list
task_list = deque([])


def add_task(task: Dict):
    task_list.append(task)


def get_ada_embedding(text):
    text = text.replace("\n", " ")
    return openai.Embedding.create(input=[text], model="text-embedding-ada-002")["data"][0]["embedding"]


def openai_call(prompt: str, use_gpt4: bool = False, temperature: float = 0.5, max_tokens: int = 100):
    if not use_gpt4:
        # Call GPT-3 DaVinci model
        response = openai.Completion.create(
            engine='text-davinci-003',
            prompt=prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        return response.choices[0].text.strip()
    else:
        # Call GPT-4 chat model
        messages = [{"role": "user", "content": prompt}]
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            n=1,
            stop=None,
        )
        return response.choices[0].message.content.strip()


def task_creation_agent(objective: str, result: Dict, task_description: str, task_list: List[str],
                        gpt_version: str = 'gpt-3'):
    prompt = f"You are an task creation AI that uses the result of an execution agent to create new tasks with the following objective: {objective}, The last completed task has the result: {result}. This result was based on this task description: {task_description}. These are incomplete tasks: {', '.join(task_list)}. Based on the result, create new tasks to be completed by the AI system that do not overlap with incomplete tasks. Return the tasks as an array."
    response = openai_call(prompt, USE_GPT4)
    new_tasks = response.split('\n')
    return [{"task_name": task_name} for task_name in new_tasks]


def prioritization_agent(this_task_id: int, gpt_version: str = 'gpt-3'):
    global task_list
    task_names = [t["task_name"] for t in task_list]
    next_task_id = int(this_task_id) + 1
    prompt = f"""You are an task prioritization AI tasked with cleaning the formatting of and reprioritizing the following tasks: {task_names}. Consider the ultimate objective of your team:{OBJECTIVE}. Do not remove any tasks. Return the result as a numbered list, like:
    #. First task
    #. Second task
    Start the task list with number {next_task_id}."""
    response = openai_call(prompt, USE_GPT4)
    new_tasks = response.split('\n')
    task_list = deque()
    for task_string in new_tasks:
        task_parts = task_string.strip().split(".", 1)
        if len(task_parts) == 2:
            task_id = task_parts[0].strip()
            task_name = task_parts[1].strip()
            task_list.append({"task_id": task_id, "task_name": task_name})


def execution_agent(objective: str, task: str, gpt_version: str = 'gpt-3') -> str:
    context = context_agent(query=objective, n=5)
    # print("\n*******RELEVANT CONTEXT******\n")
    # print(context)
    prompt = f"You are an AI software engineer who performs one task based on the following objective: {objective}.\nTake into account these previously completed tasks: {context}\nYour task: {task}\nResponse:"
    return openai_call(prompt, USE_GPT4, 0.7, 2000)


def context_agent(query: str, n: int):
    query_embedding = get_ada_embedding(query)
    results = index.query(query_embedding, top_k=n, include_metadata=True)
    # print("***** RESULTS *****")
    # print(results)
    sorted_results = sorted(results.matches, key=lambda x: x.score, reverse=True)
    return [(str(item.metadata['task'])) for item in sorted_results]

# Main loop
task_id_counter = 1

# ============GITHUB AGENT===============

# Add your GitHub API key
GITHUB_API_KEY = os.getenv("GITHUB_API_KEY", "")
assert GITHUB_API_KEY, "GITHUB_API_KEY environment variable is missing from .env"


# New functions
def login_github(token):
    return Github(token)


def list_repositories(github):
    repos = []
    for repo in github.get_user().get_repos():
        repos.append(repo.full_name)
    return repos


def list_issues(repo):
    issues = []
    for issue in repo.get_issues(state='open'):
        issues.append(issue)
    return issues


def choose_issue(issues):
    print('Issues:')
    for i, issue in enumerate(issues):
        print(f"{i + 1}. {issue.title}")
    choice = int(input("Choose an issue by its number: ")) - 1
    return issues[choice]



# Log into GitHub
print('Logging into github')
github = login_github(GITHUB_API_KEY)

# List repositories

repositories = list_repositories(github)
print('Found repositories:', repositories)
# Let user choose a repository
repository_name = input("Enter the name of the repository you want to work with:")

repo = github.get_repo(repository_name)

# List issues in the repository
issues = list_issues(repo)

# Let user choose an issue
issue = choose_issue(issues)

# create a repo object which represents the repository we are inside of
local_repo = Repo(os.getcwd())

@tool("git-branch")
def create_new_branch(branch_name: str) -> str:
    """
    Creates and checks out a new branch in the specified repository.
    """
    # Create branch
    local_repo.git.branch(branch_name)
    # Checkout branch
    local_repo.git.checkout(branch_name)

    return f"Created and checked out branch {branch_name} in {repo.name} repository."

@tool("git-commit")
def commit_to_git(file_names: str) -> str:
    """
    Takes a string of comma-separated file names and commits them to git. For example "file1.py,file2.py"
    """
    file_names = file_names.split(",")
    for file_name in file_names:
        local_repo.git.add(file_name)

    local_repo.git.commit(m="Committing changes")
    local_repo.git.push("--set-upstream", "origin", local_repo.git.branch("--show-current"))
    return f"Committed {file_names} to {repo.name} repository."

@tool("git-create-pull-request")
def create_pull_request(body) -> str:
    """
    Creates a pull request in the specified repository.
    """
    # get current branch name
    current_branch = local_repo.git.branch("--show-current")
    title="Fix for issue #" + str(issue.number)
    repo.create_pull(head=current_branch, base=repo.default_branch, issue=issue)
    return f"Created pull request for  {title} in {repo.name} repository."
llm = OpenAIChat(temperature=0, model='gpt-3.5-turbo')
tools = load_tools(["python_repl", "terminal", "serpapi"], llm=llm)
tools += [create_new_branch, commit_to_git, create_pull_request]
exec_agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

task = f"You are an AI software engineer. You are working in {os.getcwd()} on {repo.name} repository." \
       f" You must create a new branch, implement a solution and submit a pull request to address the following issue: {issue.title}.\n\n {issue.body}"
exec_agent.run(task)