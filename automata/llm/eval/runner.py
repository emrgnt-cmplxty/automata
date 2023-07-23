import json
from typing import Dict, List, Optional, Union

from automata.config import EVAL_DB_PATH, MAX_WORKERS
from automata.core.base.database import SQLDatabase
from automata.llm.eval.base import (
    Action,
    CompositeEval,
    Eval,
    EvalResult,
    check_eval_uniqueness,
)
from automata.llm.eval.metrics import EvaluationMetrics
from automata.tasks import AutomataTask, AutomataTaskExecutor


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

    TABLE_NAME = "eval_results"
    TABLE_SCHEMA = {
        "session_id": "TEXT",
        "run_id": "TEXT",
        "eval_result": "TEXT",
    }
    ENTRY_NAME = "eval_result"

    def __init__(self, db_path: str = EVAL_DB_PATH):
        self.connect(db_path)
        self.create_table(
            EvalResultWriter.TABLE_NAME,
            EvalResultWriter.TABLE_SCHEMA,
        )

    # TODO - Add run_id into full runner workflow.
    # The harness should set a run_id (or take one)
    # log it, and then use it to write and get results.
    def write_result(
        self,
        session_id: str,
        eval_result: EvalResult,
        run_id: Optional[str] = None,
    ):
        """Writes the result to the database."""
        entry = {
            "session_id": session_id,
            EvalResultWriter.ENTRY_NAME: EvalResultWriter._json_dumps_eval_result(
                eval_result.to_dict()
            ),
        }
        if run_id is not None:
            entry["run_id"] = run_id
        self.insert(EvalResultWriter.TABLE_NAME, entry)

    def get_results(self, session_id: str, run_id: Optional[str] = None):
        """Gets the results from the database"""

        filters = {}
        if session_id is not None:
            filters["session_id"] = session_id
        if run_id is not None:
            filters["run_id"] = run_id

        # TODO - Add filter on passed run_id
        results = self.select(
            EvalResultWriter.TABLE_NAME,
            [EvalResultWriter.ENTRY_NAME],
            filters,
        )

        return [
            EvalResult.from_dict(
                EvalResultWriter._json_loads_eval_result_dict(result[0])
            )
            for result in results
        ]

    # TODO - Fix type error below, requiring us to understand this error -
    # Argument 1 to "_json_dumps_recursive" of "EvalResultWriter" has
    # incompatible type "Dict[str, str]"; expected "Dict[str, Union[List[str], str, Dict[str, str]]]"
    @staticmethod
    def _json_dumps_eval_result(
        input_dict,  #: Dict[str, Union[List[str], str, Dict[str, str]]]
    ):
        """
        Function to recursively convert dictionary values to strings.
        This can be useful when we want to dump a dictionary to a JSON
        string and the dictionary contains nested dictionaries.
        """
        for key, value in input_dict.items():
            if isinstance(value, dict):
                input_dict[key] = EvalResultWriter._json_dumps_eval_result(
                    value
                )
            elif isinstance(value, list):
                input_dict[key] = [
                    EvalResultWriter._json_dumps_eval_result(v)
                    if isinstance(v, dict)
                    else v
                    for v in value
                ]
        return json.dumps(input_dict)

    @staticmethod
    def _json_loads_eval_result_dict(
        input_dict,
    ) -> Dict[str, Union[List[str], str, Dict[str, str]]]:
        """
        Function to recursively convert strings to dictionaries.
        Note, this is incapable of processing keys which are stringified dictionaries.
        # TODO - The above is how actions are stored, this approach should be considered
        """

        input_dict = json.loads(input_dict)
        for key, value in input_dict.items():
            if isinstance(value, str):
                try:
                    input_dict[
                        key
                    ] = EvalResultWriter._json_loads_eval_result_dict(value)
                except Exception:
                    pass
            elif isinstance(value, list):
                input_dict[key] = [
                    EvalResultWriter._json_loads_eval_result_dict(v)
                    if isinstance(v, dict)
                    else v
                    for v in value
                ]

        return input_dict


def process_task(
    task: AutomataTask,
    executor: AutomataTaskExecutor,
    expected_actions: List[Action],
    evals: List[Eval],
    aggregate: bool = True,
):
    results: List[EvalResult] = []
    agent = executor.execute(task)
    results.extend(
        eval.process_result(expected_actions, agent.conversation.messages)
        for eval in evals
    )
    return CompositeEval.aggregate_result(results) if aggregate else results


class EvaluationHarness:
    """A class to evaluate a list of instructions against a list of expected actions."""

    def __init__(self, evals: List[Eval], num_workers: int = MAX_WORKERS):
        check_eval_uniqueness(evals)
        self.evals = evals
        self.num_workers = num_workers

    def evaluate(
        self,
        tasks: List[AutomataTask],
        expected_actions: List[Action],
        executor: AutomataTaskExecutor,
        aggregate=True,
    ) -> EvaluationMetrics:
        """Returns the evaluation metrics for the given instructions and expected actions."""

        aggregate_results = []
        for task in tasks:
            results: List[EvalResult] = []
            agent = executor.execute(task)
            results.extend(
                eval.process_result(
                    expected_actions, agent.conversation.messages
                )
                for eval in self.evals
            )
            if aggregate:
                results = [CompositeEval.aggregate_result(results)]
            aggregate_results.extend(results)

        return EvaluationMetrics(aggregate_results)
