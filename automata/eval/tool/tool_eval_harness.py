import json
import logging
import uuid
from typing import Any, Dict, List

from tqdm import tqdm

from automata.eval.eval_base import Action, Payload
from automata.eval.tool.tool_eval import ToolEval, ToolEvalResult
from automata.eval.tool.tool_eval_metrics import ToolEvaluationMetrics
from automata.llm import FunctionCall
from automata.tools import ToolExecution


class EvalExecutionError(Exception):
    pass


class EvalLoadingError(Exception):
    pass


class ToolEvalSetLoader:
    """Loads a list of function calls and their expected actions from a JSON file."""

    def __init__(self, filepath: str):
        from automata.eval import parse_action_from_payload

        self.filepath = filepath
        if not filepath.endswith(".json"):
            raise ValueError(
                f"Only JSON files are supported, received filepath {filepath}."
            )
        payloads = self.load_json()
        self.input_functions: List[FunctionCall] = []
        self.expected_actions: List[Action] = []

        for item in payloads:
            template = item["template"]
            entries = item["entries"]

            for entry in entries:
                # TODO - Avoid using type ignore below.
                payload = self.format_values(template, entry)  # type: ignore

                input_func_call = payload.get("input_function")
                expected_action = payload.get("expected_action")

                if not isinstance(input_func_call, dict):
                    raise ValueError("Function call must be a dictionary.")
                if not isinstance(expected_action, dict):
                    raise ValueError("Expected action must be a dictionary.")

                self.input_functions.append(
                    FunctionCall(
                        name=input_func_call["name"],
                        arguments=input_func_call["arguments"],
                    )
                )
                self.expected_actions.append(
                    parse_action_from_payload(expected_action)
                )

    def format_values(self, obj: Any, formatter: Dict[str, str]) -> Any:
        """Recursively apply formatter to all string values in the object."""
        if isinstance(obj, str):
            return obj.format(**formatter)
        elif isinstance(obj, list):
            return [self.format_values(item, formatter) for item in obj]
        elif isinstance(obj, dict):
            return {
                k: self.format_values(v, formatter) for k, v in obj.items()
            }
        else:
            return obj

    def load_json(self) -> List[Payload]:
        """Loads the JSON file."""
        try:
            logging.info(f"Loading json from {self.filepath}...")
            with open(self.filepath, "r") as f:
                data = json.load(f)
            logging.info(f"Loaded {len(data)} tasks.")
            return data
        except Exception as e:
            raise EvalLoadingError from e


# TODO - Implement tool evaluation result database


class ToolEvaluationHarness:
    """A class to evaluate a list of function calls against a list of expected actions."""

    def __init__(self, evals: List[ToolEval]):
        self.evals = evals
        self.run_id = str(uuid.uuid4())

    def evaluate(
        self,
        input_functions: List[FunctionCall],
        expected_actions: List[Action],
        executor: ToolExecution,
    ) -> ToolEvaluationMetrics:
        """Returns the evaluation metrics for the given function calls and expected actions."""

        logging.info(
            f"Starting evaluation of {len(input_functions)} function calls with run_id={self.run_id}..."
        )

        aggregate_results = []
        for input_function, expected_action in tqdm(
            zip(input_functions, expected_actions)
        ):
            try:
                for eval in self.evals:
                    result = eval.generate_eval_result(
                        input_function,
                        expected_action,
                        executor,
                        run_id=self.run_id,
                    )
                    if not isinstance(result, ToolEvalResult):
                        raise ValueError(
                            "Evaluators must return a ToolEvalResult."
                        )
                    # TODO - Re-enable this once we have a database
                    # self.database.write_result(result)
                    aggregate_results.append(result)
            except Exception as e:
                logging.error(f"Error during function call execution: {e}")
                raise EvalExecutionError from e
        return ToolEvaluationMetrics(aggregate_results)
