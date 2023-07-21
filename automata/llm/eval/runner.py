import json
from typing import List

from automata.config import EVAL_DB_PATH
from automata.core.base.database import SQLDatabase
from automata.llm.eval.base import (
    Action,
    CompositeEval,
    Eval,
    EvalResult,
    check_eval_uniqueness,
)
from automata.llm.eval.metrics import EvaluationMetrics


class EvalTaskLoader:
    """Loads a list of tasks from a JSON file."""

    def __init__(self, filepath):
        self.filepath = filepath

    def load_tasks(self):
        with open(self.filepath, "r") as f:
            tasks = json.load(f)
        return tasks


class EvalResultWriter(SQLDatabase):
    """Writes evaluation results to a SQLite database."""

    def __init__(self, db_path: str = EVAL_DB_PATH):
        self.connect(db_path)
        self.create_table(
            "eval_results",
            {
                "session_id": "TEXT",
                "eval_result": "TEXT",
            },
        )

    def write_result(
        self, session_id: int, eval_result: EvalResult, conversation_id: int
    ):
        self.insert(
            "eval_results",
            {
                "session_id": session_id,
                "eval_result": json.dumps(eval_result.to_dict()),
            },
        )

    def get_results(self, session_id: int):
        results = self.select(
            "eval_results",
            ["eval_result"],
            {"session_id": session_id},
        )
        return [
            (json.loads(result), conversation_id)
            for result, conversation_id in results
        ]


class EvaluationHarness:
    """A class to evaluate a list of instructions against a list of expected actions."""

    def __init__(self, evals: List[Eval]):
        check_eval_uniqueness(evals)
        self.evals = evals

    def evaluate(
        self,
        instructions: List[str],
        expected_actions: List[List[Action]],
        aggregate=True,
    ) -> EvaluationMetrics:
        """Returns the evaluation metrics for the given instructions and expected actions."""
        results = []

        for eval, instruction, actions in zip(
            self.evals, instructions, expected_actions
        ):
            result = eval.generate_eval_result(instruction, actions)
            results.append(result)

        if aggregate:
            results = [CompositeEval.aggregate_result(results)]
        return EvaluationMetrics(results)
