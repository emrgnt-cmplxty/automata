import logging
from multiprocessing import Process

from flask import Flask, g, jsonify, request
from flask_cors import CORS

from automata.cli.cli_utils import reconfigure_logging
from automata.cli.scripts.run_task import run
from automata.config import GITHUB_API_KEY, REPOSITORY_NAME, TASK_DB_PATH
from automata.configs.config_enums import AgentConfigName
from automata.core.agent.automata_agent import AutomataAgent
from automata.core.agent.automata_database_manager import AutomataConversationDatabase
from automata.core.base.github_manager import GitHubManager
from automata.core.tasks.automata_task_executor import TaskExecutor, TestExecuteBehavior
from automata.core.tasks.automata_task_registry import AutomataTaskDatabase, AutomataTaskRegistry

logger = logging.getLogger(__name__)
GLOBAL_DEFAULT_SETTING = logging.DEBUG

app = Flask(__name__)
cors = CORS(app)


@app.before_request
def before_request():
    g.github_manager = GitHubManager(access_token=GITHUB_API_KEY, remote_name=REPOSITORY_NAME)
    g.task_registry = AutomataTaskRegistry(AutomataTaskDatabase(TASK_DB_PATH), g.github_manager)
    g.task_executor = TaskExecutor(TestExecuteBehavior(), g.task_registry)

    if request.method == "POST":
        for key in ["stream", "verbose", "include_overview"]:
            if request.form.get(key) is not None:
                request.form = request.form.copy()  # to make it mutable
                request.form.setlist(key, [request.form.get(key) == "true"])


def run_with_logs(kwargs) -> None:
    # TODO - This is a hacky way to get around the fact that the logging config is not being passed to the subprocess
    github_manager = GitHubManager(access_token=GITHUB_API_KEY, remote_name=REPOSITORY_NAME)
    task_registry = AutomataTaskRegistry(AutomataTaskDatabase(TASK_DB_PATH), github_manager)
    task_id = kwargs.get("task_id", None)
    task = task_registry.get_task_by_id(task_id)
    if not task:
        raise ValueError(f"Task with id {task_id} not found")
    task.initialize_logging()  # initialize logging in the subprocess
    run(kwargs)
    reconfigure_logging(GLOBAL_DEFAULT_SETTING)


@app.route("/tasks", methods=["GET"])
def get_all_tasks():
    tasks = g.task_registry.get_all_tasks()
    return jsonify([task.to_partial_json() for task in tasks])


@app.route("/task_summaries", methods=["GET"])
def get_all_task_summaries():
    task_summaries = g.task_registry.get_all_task_summaries()
    return jsonify(task_summaries)


@app.route("/task/<task_id>", methods=["GET"])
def get_task(task_id):
    task = g.task_registry.get_task_by_id(task_id)
    if task is None:
        return jsonify({"error": "Task not found"})
    return jsonify(task.to_partial_json())


@app.route("/task/logs/<task_id>", methods=["GET"])
def get_task_logs(task_id):
    task = g.task_registry.get_task_by_id(task_id)
    return jsonify({"logs": task.get_logs()})


@app.route("/conversation/<session_id>", methods=["GET"])
def get_conversation_no_prompt(session_id):
    conversation_db = AutomataConversationDatabase(session_id)
    full_conversations = conversation_db.get_conversations()
    cleaned_conversations = full_conversations[AutomataAgent.NUM_DEFAULT_MESSAGES :]
    return jsonify(cleaned_conversations)


@app.route("/full_conversation/<session_id>", methods=["GET"])
def get_full_conversation(session_id):
    conversation_db = AutomataConversationDatabase(session_id)
    return jsonify(conversation_db.get_conversations())


@app.route("/task/initialize", methods=["POST"])
def initialize_task():
    kwargs = {
        # "session_id": request.form.get("session_id"),
        "instructions": request.form.get("instructions"),
        "model": request.form.get("model", "gpt-4"),
        "llm_toolkits": request.form.get(
            "llm_toolkits", "python_retriever,python_writer,codebase_oracle"
        ),
        "main_config_name": request.form.get(
            "main_config_name", AgentConfigName.AUTOMATA_MAIN_DEV.value
        ),
        "helper_agent_names": request.form.get(
            "helper_agent_names",
            f"{AgentConfigName.AUTOMATA_INDEXER_DEV.value},{AgentConfigName.AUTOMATA_WRITER_DEV.value}",
        ),
        "instruction_version": request.form.get("instruction_version", "agent_introduction_dev"),
        "stream": request.form.get("stream", True),
        "verbose": request.form.get("verbose", True),
        "include_overview": request.form.get("include_overview", False),
        "generate_deterministic_id": request.form.get("generate_deterministic_id", False),
    }

    from automata.cli.scripts.run_task import initialize_task

    try:
        task = initialize_task(kwargs)
        task.initialize_logging()
        kwargs["task_id"] = str(task.task_id)
        process = Process(
            target=run_with_logs,
            args=(kwargs,),
        )
        process.start()
        reconfigure_logging(GLOBAL_DEFAULT_SETTING)
        return jsonify({"status": task.status.value, "task_id": str(task.task_id)})

    except Exception as e:
        reconfigure_logging(GLOBAL_DEFAULT_SETTING)
        return jsonify({"error": str(e)})


@app.route("/task/<task_id>/execute", methods=["POST"])
def execute_task(task_id):
    task = g.task_registry.get_task_by_id(task_id)
    task.initialize_logging()
    if task is None:
        return jsonify({"error": "Task not found"})
    try:
        g.task_executor.execute_task(task)
    except Exception as e:
        reconfigure_logging(GLOBAL_DEFAULT_SETTING)
        return jsonify({"error": str(e)})

    reconfigure_logging(GLOBAL_DEFAULT_SETTING)
    return jsonify({"message": "Task execution started"})


@app.route("/task/<task_id>/commit", methods=["POST"])
def commit_task(task_id):
    task = g.task_registry.get_task_by_id(task_id)
    task.initialize_logging()
    if task is None:
        return jsonify({"error": "Task not found"})

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
        reconfigure_logging(GLOBAL_DEFAULT_SETTING)
        return jsonify({"message": f"Task committed to {pull_url}"})
    except Exception as e:
        reconfigure_logging(GLOBAL_DEFAULT_SETTING)
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run(debug=True)
