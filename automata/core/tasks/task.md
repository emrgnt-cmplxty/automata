# Automata Task Workflow

This document provides an overview of the task workflow in the Automata repository. It covers the Task class hierarchy and how to use the TaskExecutor to execute and manage tasks.

# Task Class Hierarchy

## There are three main classes that make up the task hierarchy:

`Task`: A generic task object.

`GitHubTask`: Inherits from Task, represents a task that is to be committed to a GitHub repository.

`AutomataTask`: Inherits from GitHubTask, represents a task that is to be executed by the AutomataAgent via the TaskExecutor.

### `Task`

The Task class is a generic task object with the following attributes:

- `task_id`: A unique identifier for the task.

- `priority`: Task priority (default is 0).

- `max_retries`: Maximum number of times the task can be retried (default is 3).

- `status`: Task status, which can be one of the following TaskStatus Enum values: SETUP, PENDING, RUNNING, SUCCESS, FAILED.

- `retry_count`: Number of times the task has been retried.

### `GitHubTask`

The GitHubTask class inherits from the Task class and represents a task that is to be committed to a GitHub repository. It has the following additional attributes and methods:

- `github_manager`: A GitHubManager instance that handles interactions with the GitHub repository.
- `task_dir`: Directory path for the task.
  Methods:

- `setup_task_env()`: Creates the environment for the task.
- `commit_task(commit_message, pull_title, pull_body, pull_branch_name)`: Commits the task to the remote repository.

### `AutomataTask`

The AutomataTask class inherits from the GitHubTask class and represents a task that is to be executed by the AutomataAgent via the TaskExecutor. It has the following additional attributes:

- `rel_py_path`: Relative path to the Python file.
- `agent`: An instance of the AutomataAgent that will execute the task.
- `result`: The result of the executed task.
- `error`: An error message, if any, encountered during task execution.

### `TaskExecutor`

The TaskExecutor class is responsible for executing tasks using different behaviors defined by the IExecuteBehavior interface. The execute method of the TaskExecutor accepts an AutomataTask object and attempts to execute the task using the specified behavior. If the task fails, it will be retried according to the task's max_retries attribute using exponential backoff.

Two example behaviors are provided:

AutomataExecuteBehavior: Executes general tasks.
TestExecuteBehavior: Executes test tasks (example provided in the code).
Workflow Example
Here's an example of how to create and execute an AutomataTask:

```python
from automata.core.task.task import AutomataTask
from automata.core.base.github_manager import GitHubManager

github_manager = GitHubManager(access_token=GITHUB_API_KEY, remote_url = DEFAULT_REMOTE_URL)
executor = TaskExecutor(TestExecuteBehavior())

instruction_payload = AutomataInstructionPayload(overview="Overview", agents_message="Message")
task = AutomataTask(
    main_config=AutomataAgentConfig.load(AgentConfigName.AUTOMATA_INDEXER_DEV),
    llm_toolkits="",
    model="gpt-4",
    instruction_payload=instruction_payload,
    stream=True,
    github_manager=github_manager,rel_py_path="automata"
)

task.setup_task_env()
executor.execute(task)

rand_branch = random.randint(0, 100000)

task.commit_task(
    commit_message="This is a commit message",
    pull_title="This is a test",
    pull_body="I am testing this...",
    pull_branch_name="test_branch_%s" % (rand_branch),
)

```

In this example, we first create a `GitHubManager` instance and a `TaskExecutor` instance with the desired behavior (`TestExecuteBehavior`). Then, we create an `AutomataTask` object with the required parameters, including the `GitHubManager` instance and the relative path to the Python file.

Next, we create the task environment by calling `setup_task_env()` on the `AutomataTask` object. After that, we execute the task using the `TaskExecutor` by calling its `execute()` method and passing in the `AutomataTask` object.

Finally, after the task has been executed, we commit the task to the remote repository by calling the `commit_task()` method on the `AutomataTask` object, providing the necessary commit message, pull request title, pull request body, and branch name.

## Summary

The task workflow in the Automata repository consists of a `Task` class hierarchy and a `TaskExecutor` for executing and managing tasks. The `AutomataTask` class represents tasks that can be executed by the AutomataAgent and committed to a GitHub repository. The `TaskExecutor` class is responsible for executing tasks using different behaviors specified by the `IExecuteBehavior` interface. By following the provided example, you can create and execute tasks with various behaviors, commit the tasks to a remote repository, and handle retries in case of failures.
