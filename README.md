Overview of code in each file and what it is meant to do
Getting started guide to run the code for new users


# Overview

The improved-spork project is an AI software engineering assistant that helps developers contribute clean, high-quality code to GitHub repositories. It provides the following functionality:
* Automatically log into GitHub using an API key
* List repositories and issues
* Utilize an AI agent along with various tools (Python REPL, Terminal, and others) to close issues while adhering to the user's instructions

The project consists of the following files:
* `config.py`: Loads environment variables and stores required settings
* `custom_tools.py`: Builds custom Git tools (git-branch, git-commit, git-create-pull-request) to interact with the Git repository
* `main.py`: Logs into GitHub, selects a repository and issue, initializes the AI agent, and runs the task of closing the chosen issue
* `utils.py`: Contains utility functions for GitHub interactions


# Getting Started

To run the code, follow these steps:

1. Clone the repository on your local machine.
2. Navigate to the project directory.
3. Run `python file1.py` to execute the main script.