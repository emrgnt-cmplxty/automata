from typing import List, Optional

from automata.config import EVAL_DB_PATH
from automata.core.base.database import SQLDatabase
from automata.eval.agent.agent_eval import AgentEvalResult
from automata.eval.agent.agent_eval_harness import create_payload, load_payload


class AgentEvalResultDatabase(SQLDatabase):
    """Writes evaluation results to a SQLite database."""

    TABLE_NAME = "eval_results"
    ENTRY_NAME = "eval_result"
    TABLE_SCHEMA = {
        "session_id": "TEXT",
        "run_id": "TEXT",
        ENTRY_NAME: "TEXT",
    }

    def __init__(self, db_path: str = EVAL_DB_PATH):
        self.connect(db_path)
        self.create_table(
            AgentEvalResultDatabase.TABLE_NAME,
            AgentEvalResultDatabase.TABLE_SCHEMA,
        )

    # TODO - Add run_id into full runner workflow.
    # The harness should set a run_id (or take one)
    # log it, and then use it to write and get results.
    def write_result(
        self,
        eval_result: AgentEvalResult,
    ) -> None:
        """Writes the result to the database."""

        if not eval_result.session_id:
            raise ValueError(
                "Session ID must be set to save an evaluation result."
            )

        entry = {
            "session_id": eval_result.session_id,
            AgentEvalResultDatabase.ENTRY_NAME: create_payload(
                eval_result.to_payload()
            ),
        }
        # TODO - This is a hack to avoid complicated filtering
        # logic necessary to filter eval by run_id, we should
        # fix later.
        entry["run_id"] = eval_result.run_id
        self.insert(AgentEvalResultDatabase.TABLE_NAME, entry)

    def get_results(
        self, session_id: Optional[str] = None, run_id: Optional[str] = None
    ) -> List[AgentEvalResult]:
        """Gets the results from the database"""

        filters = {}
        if not session_id and not run_id:
            raise ValueError("Must provide session_id or run_id.")

        if session_id is not None:
            filters["session_id"] = session_id

        if run_id is not None:
            filters["run_id"] = run_id

        # TODO - Add filter on passed run_id
        entries = self.select(
            AgentEvalResultDatabase.TABLE_NAME,
            [AgentEvalResultDatabase.ENTRY_NAME, "session_id", "run_id"],
            filters,
        )
        results: List[AgentEvalResult] = []
        for entry in entries:
            payload = load_payload(entry[0])
            if not isinstance(payload, dict):
                raise ValueError("Loaded payload should be a dictionary.")
            payload["session_id"] = entry[1]
            payload["run_id"] = entry[2]
            results.append(AgentEvalResult.from_payload(payload))

        return results
