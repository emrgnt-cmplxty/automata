from itertools import chain
from multiprocessing import Pool
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
from automata.tasks import AutomataTask, AutomataTaskExecutor
from automata.config import MAX_WORKERS

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
        print(results)  # Debugging code

        return [
            json.loads(result[0])
            for result in results
        ]


class EvaluationHarness:
    """A class to evaluate a list of instructions against a list of expected actions."""

    def __init__(self, evals: List[Eval], num_workers: int=MAX_WORKERS):
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

        # aggregate_results = []
        # for task in tasks:
        #     results: List[EvalResult] = []
        #     agent = executor.execute(task)
        #     results.extend(
        #         eval.process_result(
        #             expected_actions, agent.conversation.messages
        #         )
        #         for eval in self.evals
        #     )
        #     if aggregate:
        #         results = [CompositeEval.aggregate_result(results)]
        #     aggregate_results.extend(results)

        # return EvaluationMetrics(aggregate_results)

        # Define a function to process a single task
        def process_task(task):
            results: List[EvalResult] = []
            agent = executor.execute(task)
            results.extend(
                eval.process_result(
                    expected_actions, agent.conversation.messages
                )
                for eval in self.evals
            )
            if aggregate:
                return CompositeEval.aggregate_result(results)
            return results

        # Create a multiprocessing pool and map the process_task function to all tasks
        with Pool() as p:
            aggregate_results = p.map(process_task, tasks)

        # Flatten the results if necessary
        aggregate_results = list(chain(*aggregate_results))

        return EvaluationMetrics(aggregate_results)
