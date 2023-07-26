"""A module for executing a list of instructions from memory or disk."""
import contextlib
import json
import logging
from typing import Dict, List, Union, cast

from automata.eval.base import (
    Action,
    AgentEval,
    AgentEvalResult,
    Payload,
    parse_action_from_payload,
)
from automata.eval.composite import (
    aggregate_agent_result,
    check_eval_uniqueness,
)
from automata.eval.error import EvalExecutionError, EvalLoadingError
from automata.eval.metrics import AgentEvaluationMetrics
from automata.tasks import AutomataTask, AutomataTaskExecutor

logger = logging.getLogger(__name__)


class AgentEvalSetLoader:
    """Loads a list of tasks from a JSON file."""

    def __init__(self, filepath: str):
        # sourcery skip: docstrings-for-functions
        self.filepath = filepath
        if not filepath.endswith(".json"):
            raise ValueError(
                f"Only JSON files are supported, received filepath {filepath}"
            )
        payloads = self.load_json()
        self.tasks: List[AutomataTask] = []
        self.tasks_expected_actions: List[List[Action]] = []

        for payload in payloads:
            instructions = payload.get("instructions")
            expected_actions = payload.get("expected_actions")

            assert isinstance(
                instructions, str
            ), "instructions must be a string"
            assert isinstance(
                expected_actions, list
            ), "expected_actions must be a dictionary"
            for expected_action in expected_actions:
                assert isinstance(
                    expected_action, dict
                ), "each expected action must be a dictionary"

            self.tasks.append(AutomataTask(instructions=instructions))
            self.tasks_expected_actions.append(
                [
                    parse_action_from_payload(action)  # type: ignore
                    for action in expected_actions
                ]
            )

    def load_json(self) -> List[Payload]:
        """Loads the JSON file."""

        try:
            logging.info(f"Loading json from {self.filepath}...")
            with open(self.filepath, "r") as f:
                json_output = json.load(f)
            logging.info(f"Loaded {len(json_output)} tasks.")
        except Exception as e:
            raise EvalLoadingError from e
        return json_output


def create_payload(input_dict: Payload) -> str:
    """
    Function to recursively convert dictionary values to strings.
    This can be useful when we want to dump a dictionary to a JSON
    string and the dictionary contains nested dictionaries.
    """

    for key, value in input_dict.items():
        if isinstance(value, dict):
            cast_value = cast(Payload, value)  # TODO - Why do we need to cast?
            input_dict[key] = create_payload(cast_value)
        elif isinstance(value, list):
            input_dict[key] = [
                create_payload(v) if isinstance(v, dict) else v for v in value
            ]
    return json.dumps(input_dict)


def load_payload(
    input_payload: Union[str, Dict[str, str]],
) -> Payload:
    """
    Function to recursively convert strings to dictionaries.
    Note, this is incapable of processing keys which are stringified dictionaries.
    """

    payload = (
        json.loads(input_payload)
        if isinstance(input_payload, str)
        else input_payload
    )

    for key, value in payload.items():
        if isinstance(value, str):
            with contextlib.suppress(Exception):
                payload[key] = load_payload(value)
        elif isinstance(value, list):
            payload[key] = [
                load_payload(v) if isinstance(v, dict) else v for v in value
            ]

    return payload


def process_task(
    task: AutomataTask,
    executor: AutomataTaskExecutor,
    expected_actions: List[Action],
    evals: List[AgentEval],
    aggregate: bool = True,
) -> Union[List[AgentEvalResult], AgentEvalResult]:
    """Processes a single task and returns the evaluation results."""

    results: List[AgentEvalResult] = []
    agent = executor.execute(task)
    for eval in evals:
        result = eval.process_result(
            expected_actions,
            agent.conversation.messages,
            session_id=agent.session_id,
        )
        if not isinstance(result, AgentEvalResult):
            raise ValueError("Evaluators must return an AgentEvalResult.")
        results.append(result)
    return aggregate_agent_result(results) if aggregate else results


class AgentEvaluationHarness:
    """A class to evaluate a list of instructions against a list of expected actions."""

    def __init__(self, evals: List[AgentEval]):
        check_eval_uniqueness(evals)
        self.evals = evals
        # self.num_workers = num_workers # TODO - Include parallelizatio

    def evaluate(
        self,
        tasks: List[AutomataTask],
        tasks_expected_actions: List[List[Action]],
        executor: AutomataTaskExecutor,
        aggregate: bool = True,
    ) -> AgentEvaluationMetrics:
        """Returns the evaluation metrics for the given instructions and expected actions."""

        logging.info(f"Starting evaluation of {len(tasks)} tasks...")

        aggregate_results = []
        for task, expected_actions in zip(tasks, tasks_expected_actions):
            try:
                results: List[AgentEvalResult] = []
                agent = executor.execute(task)
                for eval in self.evals:
                    result = eval.process_result(
                        expected_actions,
                        agent.conversation.messages,
                        session_id=agent.session_id,
                    )
                    if not isinstance(result, AgentEvalResult):
                        raise ValueError(
                            "Evaluators must return an AgentEvalResult."
                        )
                    results.append(result)
                if aggregate:
                    results = [aggregate_agent_result(results)]
                aggregate_results.extend(results)

            except Exception as e:
                logging.error(f"Error during task execution: {e}")
                raise EvalExecutionError from e

        logging.info("Evaluation complete, calculating metrics...")

        return AgentEvaluationMetrics(aggregate_results)
