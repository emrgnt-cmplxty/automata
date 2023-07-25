import json
import logging
from typing import Dict, List, Optional, Union, cast

from automata.config import EVAL_DB_PATH
from automata.core.base.database import SQLDatabase
from automata.eval.base import (
    Action,
    CompositeEval,
    Eval,
    EvalResult,
    check_eval_uniqueness,
)
from automata.eval.error import EvalExecutionError, EvalLoadingError
from automata.eval.metrics import EvaluationMetrics
from automata.tasks import AutomataTask, AutomataTaskExecutor

logger = logging.getLogger(__name__)


class EvalTaskLoader:
    """Loads a list of tasks from a JSON file."""

    def __init__(self, filepath):
        self.filepath = filepath
        self.tasks = self.load_json()

    def load_json(self) -> Dict[str, Union[str, List[str]]]:
        """Loads the JSON file."""
        try:
            logging.info(f"Loading json from {self.filepath}...")
            with open(self.filepath, "r") as f:
                json_output = json.load(f)
            logging.info(f"Loaded {len(json_output)} tasks.")
        except Exception as e:
            raise EvalLoadingError from e
        return json_output


class EvalResultDatabase(SQLDatabase):
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
            EvalResultDatabase.TABLE_NAME,
            EvalResultDatabase.TABLE_SCHEMA,
        )

    # TODO - Add run_id into full runner workflow.
    # The harness should set a run_id (or take one)
    # log it, and then use it to write and get results.
    def write_result(
        self,
        eval_result: EvalResult,
        run_id: Optional[str] = None,
    ) -> None:
        """Writes the result to the database."""

        if not eval_result.session_id:
            raise ValueError(
                "Session ID must be set to save an evaluation result."
            )

        entry = {
            "session_id": eval_result.session_id,
            EvalResultDatabase.ENTRY_NAME: EvalResultDatabase._create_payload(
                eval_result.to_dict()
            ),
        }
        if run_id is not None:
            entry["run_id"] = run_id
        self.insert(EvalResultDatabase.TABLE_NAME, entry)

    def get_results(
        self, session_id: str, run_id: Optional[str] = None
    ) -> List[EvalResult]:
        """Gets the results from the database"""

        filters = {}
        if session_id is not None:
            filters["session_id"] = session_id
        if run_id is not None:
            filters["run_id"] = run_id

        # TODO - Add filter on passed run_id
        results = self.select(
            EvalResultDatabase.TABLE_NAME,
            [EvalResultDatabase.ENTRY_NAME],
            filters,
        )

        return [
            EvalResult.from_payload(
                EvalResultDatabase._load_payload(result[0])
            )
            for result in results
        ]

    @staticmethod
    def _create_payload(
        input_dict: Dict[str, Union[List[str], str, Dict[str, str]]]
    ) -> str:
        """
        Function to recursively convert dictionary values to strings.
        This can be useful when we want to dump a dictionary to a JSON
        string and the dictionary contains nested dictionaries.
        """

        for key, value in input_dict.items():
            if isinstance(value, dict):
                cast_value = cast(
                    Dict[str, Union[List[str], str, Dict[str, str]]], value
                )  # TODO - Why do we need to cast?
                input_dict[key] = EvalResultDatabase._create_payload(
                    cast_value
                )
            elif isinstance(value, list):
                input_dict[key] = [
                    EvalResultDatabase._create_payload(v)
                    if isinstance(v, dict)
                    else v
                    for v in value
                ]
        return json.dumps(input_dict)

    @staticmethod
    def _load_payload(
        input_dict,
    ) -> Dict[str, Union[List[str], str, Dict[str, str]]]:
        """
        Function to recursively convert strings to dictionaries.
        Note, this is incapable of processing keys which are stringified dictionaries.
        """

        input_dict = json.loads(input_dict)
        for key, value in input_dict.items():
            if isinstance(value, str):
                try:
                    input_dict[key] = EvalResultDatabase._load_payload(value)
                except Exception:
                    pass
            elif isinstance(value, list):
                input_dict[key] = [
                    EvalResultDatabase._load_payload(v)
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
) -> Union[List[EvalResult], EvalResult]:
    results: List[EvalResult] = []
    agent = executor.execute(task)
    results.extend(
        eval.process_result(
            expected_actions, agent.conversation.messages, agent.session_id
        )
        for eval in evals
    )
    return CompositeEval.aggregate_result(results) if aggregate else results


class EvaluationHarness:
    """A class to evaluate a list of instructions against a list of expected actions."""

    def __init__(self, evals: List[Eval]):
        check_eval_uniqueness(evals)
        self.evals = evals
        # self.num_workers = num_workers # TODO - Include parallelizatio

    def evaluate(
        self,
        tasks: List[AutomataTask],
        expected_actions: List[Action],
        executor: AutomataTaskExecutor,
        aggregate=True,
    ) -> EvaluationMetrics:
        """Returns the evaluation metrics for the given instructions and expected actions."""

        logging.info(f"Starting evaluation of {len(tasks)} tasks...")

        aggregate_results = []
        for task in tasks:
            try:
                results: List[EvalResult] = []
                agent = executor.execute(task)
                results.extend(
                    eval.process_result(
                        expected_actions,
                        agent.conversation.messages,
                        agent.session_id,
                    )
                    for eval in self.evals
                )
                if aggregate:
                    results = [CompositeEval.aggregate_result(results)]
                aggregate_results.extend(results)

            except Exception as e:
                logging.error("Error during task execution: ", e)
                raise EvalExecutionError from e

        logging.info("Evaluation complete, calculating metrics...")

        return EvaluationMetrics(aggregate_results)
