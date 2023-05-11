import os

from flask import Flask, g, jsonify, request
from flask_cors import CORS

from automata.config import DEFAULT_REMOTE_URL, GITHUB_API_KEY, TASK_DB_NAME
from automata.configs.config_enums import AgentConfigVersion
from automata.core.base.github_manager import GitHubManager
from automata.core.tasks.task import TaskStatus
from automata.core.tasks.task_registry import AutomataTaskDatabase, TaskRegistry
from automata.core.utils import Namespace, root_path

app = Flask(__name__)
cors = CORS(app)


@app.before_request
def before_request():
    g.github_manager = GitHubManager(access_token=GITHUB_API_KEY, remote_url=DEFAULT_REMOTE_URL)
    g.task_registry = TaskRegistry(
        AutomataTaskDatabase(os.path.join(root_path(), TASK_DB_NAME)), g.github_manager
    )

    if request.method == "POST":
        for key in ["stream", "verbose", "include_overview"]:
            if request.form.get(key) is not None:
                request.form = request.form.copy()  # to make it mutable
                request.form.setlist(key, [request.form.get(key) == "true"])


@app.route("/master", methods=["POST"])
def master():
    print("request.form = ", request.form)
    kwargs = {
        "session_id": request.form.get("session_id"),
        "instructions": request.form.get("instructions"),
        "model": request.form.get("model", "gpt-4"),
        "llm_toolkits": request.form.get(
            "llm_toolkits", "python_indexer,python_writer,codebase_oracle"
        ),
        "master_config_version": request.form.get(
            "master_config_version", AgentConfigVersion.AUTOMATA_MASTER_DEV.value
        ),
        "agent_config_versions": request.form.get(
            "agent_config_versions",
            f"{AgentConfigVersion.AUTOMATA_INDEXER_DEV.value},{AgentConfigVersion.AUTOMATA_WRITER_DEV.value}",
        ),
        "stream": request.form.get("stream", True),
        "verbose": request.form.get("verbose", True),
        "instruction_version": request.form.get("instruction_version", "agent_introduction_dev"),
        "include_overview": request.form.get("include_overview", True),
    }
    from automata.cli.scripts.run_coordinator import main

    print("Calling main with args = ", kwargs)
    namespace = Namespace(**kwargs)
    result = main(namespace)
    return jsonify(result)


@app.route("/evaluator", methods=["POST"])
def evaluator():
    kwargs = {
        "instructions": request.form.get("instructions"),
        "model": request.form.get("model", "gpt-4"),
        "session_id": request.form.get("session_id"),
        "llm_toolkits": request.form.get(
            "llm_toolkits", "python_indexer,python_writer,codebase_oracle"
        ),
        "master_config_version": request.form.get(
            "master_config_version", AgentConfigVersion.AUTOMATA_MASTER_DEV.value
        ),
        "agent_config_versions": request.form.get(
            "agent_config_versions",
            f"{AgentConfigVersion.AUTOMATA_INDEXER_DEV.value},{AgentConfigVersion.AUTOMATA_WRITER_DEV.value}",
        ),
        "stream": request.form.get("stream", True),
        "verbose": request.form.get("verbose", False),
        "eval_config": request.form.get("eval_config", "python_indexer_payload"),
    }
    from automata.cli.scripts.run_evaluator import main

    namespace = Namespace(**kwargs)
    result = main(namespace)
    return jsonify(result)


@app.route("/tasks", methods=["GET"])
def get_all_tasks():
    tasks = g.task_registry.get_all_tasks()
    print("tasks = ", tasks)
    task = tasks[-1]
    print("task.__dict__ = ", task.__dict__)
    print("tasks[0].task_id = ", tasks[-1].task_id)
    print("tasks[0].status = ", tasks[-1].status)
    print("tasks[0].builder = ", tasks[-1].builder)
    print("tasks[0].builder.instance = ", tasks[-1].builder._instance)
    print(
        "tasks[0].builder._instance.instruction_payload = ",
        tasks[-1].builder._instance.instruction_payload,
    )
    tasks_as_dict = [task.__dict__ for task in tasks]
    return jsonify(tasks_as_dict)


@app.route("/task/<task_id>/initialize", methods=["POST"])
def initialize_task(task_id):
    task = g.task_registry.get_task(task_id)
    if task is None:
        return jsonify({"error": "Task not found"}), 404
    task.status = TaskStatus.SETUP  # Assuming setting the status to SETUP initializes the task
    return jsonify({"message": "Task initialized"})


@app.route("/task/<task_id>/execute", methods=["POST"])
def execute_task(task_id):
    task = g.task_registry.get_task(task_id)
    if task is None:
        return jsonify({"error": "Task not found"}), 404
    # Assuming execute() is a method of AutomataTask that starts the task execution
    try:
        task.execute()
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify({"message": "Task execution started"})


def commit_task(task_id):
    task = g.task_registry.get_task(task_id)
    if task is None:
        return jsonify({"error": "Task not found"}), 404

    commit_data = request.get_json()
    commit_message = commit_data.get("commit_message", "")
    pull_title = commit_data.get("pull_title", "")
    pull_body = commit_data.get("pull_body", "")
    pull_branch_name = commit_data.get("pull_branch_name", "feature/test")

    try:
        g.task_registry.commit_task(
            task, g.github_manager, commit_message, pull_title, pull_body, pull_branch_name
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"message": "Task committed"})


@app.route("/task/<task_id>/logs", methods=["GET"])
def get_task_logs(task_id):
    task = g.task_registry.get_task(task_id)
    if task is None:
        return jsonify({"error": "Task not found"}), 404
    # Assuming logs are stored as a list of strings in a 'logs' attribute of the AutomataTask
    return jsonify({"logs": task.logs})


if __name__ == "__main__":
    app.run(debug=True)
