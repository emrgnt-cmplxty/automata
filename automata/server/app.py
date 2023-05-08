from flask import Flask, jsonify, request

from automata.configs.config_enums import AgentConfigVersion
from automata.core.utils import Namespace

app = Flask(__name__)


@app.route("/master", methods=["POST"])
def master():
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


if __name__ == "__main__":
    app.run(debug=True)
