Automata Code Repository

This repository contains a collection of tools and utilities for various tasks.

Main Packages and Modules:

1. automata.core.agent.automata_agent:
   AutomataAgent is an autonomous agent that performs the actual work of the Automata system. Automata are responsible for executing instructions and reporting the results back to the master.

2. automata.core.agent.master_automata_agent:
   MasterAutomataAgent is a specialized AutomataAgent that can interact with an AutomataCoordinator to execute and manipulate other AutomataAgents as part of the conversation.

3. automata.core.agent.automata_agent_builder:
   AutomataAgentBuilder is a class for building and configuring AutomataAgent instances.

4. automata.core.coordinator.automata_coordinator:
   AutomataCoordinator is a class for managing the interactions between multiple AutomataAgents.

5. automata.tools.python_tools.python_indexer:
   A module providing functionality to extract information about classes, functions, and their docstrings from a given directory of Python files. It defines the `PythonIndexer` class that can be used to get the source code, docstrings, and list of functions or classes within a specific file.

6. automata.tools.python_tools.python_writer:
   A module which provides the ability to change the in-memory representation of a python module in the PythonIndexer and to
   write this out to disk

7. automata.tools.oracle.codebase_oracle:
   A codebase oracle module. The documentation for this module is currently unavailable.

# Getting Started

To run the code, follow these steps:

1. Clone the repository on your local machine.
2. Navigate to the project directory.
3. Create and activate a virtual environment by running `python3 -m venv local_env && source local_env/bin/activate`
4. Upgrade to the latest pip by running `python3 -m pip install --upgrade pip`
5. Install the project in editable mode by running `pip3 install -e .`
6. Install pre-commit hooks by running `pre-commit install`
7. Build appropriate .env file
8. Execute the main script as in this example - `automata master --instructions="Query the indexer agent for the class AutomataMasterAgent's method 'run' and return the raw code code" -v`

# References

## Automata Agent CLI

The Automata Agent CLI provides a simple and convenient way to interact with the agent. The available commands and options can be found in the [Automata Agent CLI Documentation](automata/cli/cli.md).

## Automata Agent

The AutomataAgent is an autonomous agent designed to execute instructions and report the results back to the master system. It communicates with the OpenAI API to generate responses based on given instructions and manages interactions with various tools. More information can be found in the [Automata Agent Documentation](automata/core/agent/agent.md).

## Automata Coordinator

The AutomataCoordinator is responsible for managing multiple AutomataAgents, including the MasterAutomataAgent. It allows them to work together to perform various tasks and generate results. The AutomataInstance is a representation of an AutomataAgent, including its configuration, description, and builder class. More information can be found in the [Automata Coordinator Documentation](automata/core/coordinator/coordinator.md).

## Automata Tools

The AutomataTools provide capabilities to index, write, and search Python codebases. This documentation covers PythonIndexer, PythonWriter, and CodeBaseOracle classes, which are part of the AutomataTools. More information can be found in the [Automata Tools Documentation](automata/tools/tools.md).

## Automata Tool Management

This Automata Tool Management workflow provides agents with managers that interact with different APIs and provide functionality to read and modify the code state of Python files, build low-level manipulation (LLM) toolkits, and facilitate code searches. More information can be found in the [Automata Tool Management Documentation](automata/tool_management/tool_management.md).

## Automata Task Management

This Automata repository provides a task workflow. It covers the Task class hierarchy and how to use the TaskExecutor to execute and manage tasks. More information can be found here [Automata Task Documentation](automata/core/tasks/task.md).

## Evaluation Suite

The Eval class is a base class for evaluating the performance of an AutomataAgent given a set of instructions. It provides methods for generating evaluation results and extracting actions from the agent's responses. Subclasses of the Eval class should override the eval_sample and run methods to customize evaluation behavior. More information can be found in the [Automata Eval Documentation](automata/evals/eval.md).
