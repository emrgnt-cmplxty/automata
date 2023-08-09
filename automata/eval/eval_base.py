import logging
import uuid
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Type, Union

import automata.core.utils  # pylint: disable=unused-import

logger = logging.getLogger(__name__)

Payload = Dict[str, Union[List[str], str, Dict[str, str]]]


class Action(ABC):
    """An arbitrary action to be taken by an LLM, like an OpenAI function call"""

    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def to_payload(self) -> Payload:
        """Converts the Action to a dictionary."""
        pass

    @staticmethod
    @abstractmethod
    def from_payload(dct: Payload) -> "Action":
        """Creates an Action from a dictionary."""
        pass


ACTION_REGISTRY = {}


def register_action(cls: Type[Action]) -> Type[Action]:
    """
    A decorator for registering an Action subclass in the ACTION_REGISTRY
    """
    ACTION_REGISTRY[cls.__name__] = cls
    return cls


def parse_action_from_payload(payload: Payload) -> Action:
    """Parses out the corresponding action from a raw dictionary."""
    action_type = payload.pop("type")
    if isinstance(action_type, str):
        ActionClass = ACTION_REGISTRY.get(action_type)
        if ActionClass is None:
            raise ValueError(f"Unknown action type: {action_type}")
        return ActionClass.from_payload(payload)
    else:
        raise ValueError("Action type must be a string.")


class EvalResult(ABC):
    """An abstract class to represent the result of an evaluation."""

    def __init__(self, *args, **kwargs):
        # TODO - Add tests for run_id
        self.run_id = kwargs.get("run_id") or str(uuid.uuid4())
        if not isinstance(self.run_id, str):
            raise ValueError("run_id must be a string.")

    @property
    @abstractmethod
    def is_full_match(self) -> bool:
        """Indicates whether the evaluation was a full match."""

    @property
    @abstractmethod
    def is_partial_match(self) -> bool:
        """Indicates whether the evaluation was a partial match."""

    @abstractmethod
    def to_payload(self) -> Payload:
        """Converts the evaluation result to a dictionary (or other serializable format)."""

    @classmethod
    @abstractmethod
    def from_payload(cls, payload: Payload) -> "EvalResult":
        """Creates an evaluation result from a dictionary (or other serialized format)."""


class Eval(ABC):
    """Abstract class for evaluating an LLMs performance."""

    @abstractmethod
    def __init__(
        self,
        *args,
        **kwargs,
    ):
        pass

    @abstractmethod
    def generate_eval_result(
        self,
        exec_input: Any,
        expected_output: Any,
        executor: Any,
        *args,
        **kwargs,
    ) -> EvalResult:
        """Generates an eval result for a given set of instructions and expected actions."""
        pass

    @abstractmethod
    def extract_action(self, input: Any) -> Any:
        """Extracts a list of action from the given message."""
        pass

    @abstractmethod
    def _filter_actions(self, inputs: Any) -> Any:
        """Filters a list of actions to only contain actions that are relevant to the eval."""
        pass
