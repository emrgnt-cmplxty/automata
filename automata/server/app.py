from multiprocessing import Process

from flask import Flask, g, jsonify, request
from flask_cors import CORS

from automata.config import GITHUB_API_KEY, REPOSITORY_NAME, TASK_DB_PATH
from automata.configs.config_enums import AgentConfigVersion
from automata.core.base.github_manager import GitHubManager
from automata.core.tasks.task_executor import TaskExecutor, TestExecuteBehavior
from automata.core.tasks.task_registry import AutomataTaskDatabase, TaskRegistry

app = Flask(__name__)
cors = CORS(app)


@app.before_request
def before_request():
    g.github_manager = GitHubManager(access_token=GITHUB_API_KEY, remote_name=REPOSITORY_NAME)
    g.task_registry = TaskRegistry(AutomataTaskDatabase(TASK_DB_PATH), g.github_manager)
    g.task_executor = TaskExecutor(TestExecuteBehavior(), g.task_registry)

    if request.method == "POST":
        for key in ["stream", "verbose", "include_overview"]:
            if request.form.get(key) is not None:
                request.form = request.form.copy()  # to make it mutable
                request.form.setlist(key, [request.form.get(key) == "true"])


@app.route("/tasks", methods=["GET"])
def get_all_tasks():
    tasks = g.task_registry.get_all_tasks()
    return jsonify([task.to_partial_json() for task in tasks])


@app.route("/task/<task_id>", methods=["GET"])
def get_task(task_id):
    task = g.task_registry.get_task_by_id(task_id)
    if task is None:
        return jsonify({"error": "Task not found"}), 404
    return jsonify(task.to_partial_json())


@app.route("/task", methods=["POST"])
def initialize_task():
    kwargs = {
        "session_id": request.form.get("session_id"),
        "instructions": request.form.get("instructions"),
        "model": request.form.get("model", "gpt-4"),
        "llm_toolkits": request.form.get(
            "llm_toolkits", "python_indexer,python_writer,codebase_oracle"
        ),
        "main_config_name": request.form.get(
            "main_config_name", AgentConfigVersion.AUTOMATA_MAIN_DEV.value
        ),
        "helper_agent_names": request.form.get(
            "helper_agent_names",
            f"{AgentConfigVersion.AUTOMATA_INDEXER_DEV.value},{AgentConfigVersion.AUTOMATA_WRITER_DEV.value}",
        ),
        "instruction_version": request.form.get("instruction_version", "agent_introduction_dev"),
        "stream": request.form.get("stream", True),
        "verbose": request.form.get("verbose", True),
        "include_overview": request.form.get("include_overview", False),
        "generate_deterministic_id": request.form.get("generate_deterministic_id", False),
    }
    from automata.cli.scripts.run_task import initialize_task, run

    try:
        task = initialize_task(kwargs)
        print("task.status = ", task.status)
        print("task.task_dir = ", task.task_dir)
        process = Process(target=run, args=(str(task.task_id), kwargs))
        print("running with process = ", process)
        process.start()
        return jsonify({"status": task.status.value, "task_id": str(task.task_id)})

    except Exception as e:
        print("error = ", e)
        return jsonify({"error": str(e)}), 500


@app.route("/task/<task_id>/execute", methods=["POST"])
def execute_task(task_id):
    task = g.task_registry.get_task_by_id(task_id)
    if task is None:
        return jsonify({"error": "Task not found"}), 404
    try:
        g.task_executor.execute_task(task)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify({"message": "Task execution started"})


@app.route("/task/<task_id>/commit", methods=["POST"])
def commit_task(task_id):
    task = g.task_registry.get_task_by_id(task_id)
    if task is None:
        return jsonify({"error": "Task not found"}), 404

    commit_data = request.get_json()
    commit_message = commit_data.get("commit_message", "")
    pull_title = commit_data.get("pull_title", "")
    pull_body = commit_data.get("pull_body", "")
    pull_branch_name = commit_data.get("pull_branch_name", "feature/test")
    github_manager = GitHubManager(access_token=GITHUB_API_KEY, remote_name=REPOSITORY_NAME)
    try:
        pull_url = g.task_registry.commit_task(
            task, github_manager, commit_message, pull_title, pull_body, pull_branch_name
        )
        return jsonify({"message": f"Task committed to {pull_url}"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
