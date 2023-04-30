Automata Code Repository

This repository contains a collection of tools and utilities for various tasks.

Main Packages and Modules:

1. automata.main_automata:
   The main package for the Automata project. It currently has no documentation.

2. automata.tools.prompts:
   A module containing task generators for planning and execution agents.
   Functions:

   - make_planning_task: A function for generating a planning task for an agent.
   - make_execution_task: A function for generating an execution task for an agent.

3. automata.core.utils:
   A module providing functions to interact with the GitHub API. It includes listing repositories, issues, and pull requests, choosing a work item, and removing HTML tags from text.

4. automata.tools.python_tools.python_indexer:
   A module providing functionality to extract information about classes, functions, and their docstrings from a given directory of Python files. It defines the `PythonIndexer` class that can be used to get the source code, docstrings, and list of functions or classes within a specific file.

5. automata.tools.python_tools.python_writer:
   A module which provides the ability to change the in-memory representation of a python module in the PythonIndexer and to
   write this out to disk

6. automata.tools.documentation.documentation_gpt:
   A simple chatbot that uses DocGPT to answer questions about documentation.

7. automata.tools.oracle.codebase_oracle:
   A codebase oracle module. The documentation for this module is currently unavailable.

8. automata.core.agent.automata_agent:
   AutomataAgent is an autonomous agent that performs the actual work of the Automata system. Automata are responsible for executing instructions and reporting the results back to the master.

# Getting Started

To run the code, follow these steps:

1. Clone the repository on your local machine.
2. Navigate to the project directory.
3. Create and activate a virtual environment by running `python3 -m venv local_env && source local_env/bin/activate`
4. Upgrade to the latest pip by running `python3 -m pip install --upgrade pip`
5. Install the project in editable mode by running `pip3 install -e .`
6. Install pre-commit hooks by running `pre-commit install`
7. Build appropriate .env file
8. Execute the main script by running `python -m automata.main_coordinator ...[INSERT ARGS]`
