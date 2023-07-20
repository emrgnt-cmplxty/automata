import json
from typing import List

from automata.core.base.database import SQLDatabase
from automata.llm.eval.base import (
    Action,
    CompositeEval,
    Eval,
    check_eval_uniqueness,
)
from automata.llm.eval.metrics import EvaluationMetrics

# Evaluation task loader


class EvalTaskLoader:
    def __init__(self, filepath):
        self.filepath = filepath

    def load_tasks(self):
        with open(self.filepath, "r") as f:
            tasks = json.load(f)
        return tasks


# Evaluation result writer


class EvalResultWriter(SQLDatabase):
    def __init__(self, db_path):
        self.connect(db_path)
        self.create_table(
            "eval_results",
            {
                "session_id": "TEXT",
                "eval_result": "TEXT",
                "conversation_id": "TEXT",
            },
        )

    def write_result(self, session_id, eval_result, conversation_id):
        self.insert(
            "eval_results",
            {
                "session_id": session_id,
                "eval_result": json.dumps(eval_result._asdict()),
                "conversation_id": conversation_id,
            },
        )

    def get_results(self, session_id):
        results = self.select(
            "eval_results",
            ["eval_result", "conversation_id"],
            {"session_id": session_id},
        )
        return [
            (json.loads(result), conversation_id)
            for result, conversation_id in results
        ]


# Modified EvaluationHarness

# class EvaluationHarness:
#     def __init__(self, evaluators, session_id, db_path):
#         self.evaluators = evaluators
#         self.session_id = session_id
#         self.result_writer = EvalResultWriter(db_path)

#     def run_and_log_evaluations(self, payload: Dict[str, Any]) -> List[EvalResult]:
#         instructions = payload['instructions']
#         expected_actions = payload['expected_actions']
#         results = []
#         for evaluator in self.evaluators:
#             # evaluator.agent_provider.set_database_provider(LLMConversationDatabaseProvider(self.session_id))
#             result = evaluator.generate_eval_result(instructions, expected_actions)
#             results.append(result)
#             # self.result_writer.write_result(self.session_id, result, evaluator.agent_provider.get_conversation_id())
#         return results


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
            print(f"result = {result}")
            print(f"result.extra_actions = {result.extra_actions}")
            results.append(result)

        if aggregate:
            results = [CompositeEval.aggregate_result(results)]
        return EvaluationMetrics(results)
