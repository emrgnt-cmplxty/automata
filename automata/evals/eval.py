import abc
import logging
from typing import List

from automata.core.agent.automata_action_extractor import AutomataActionExtractor
from automata.core.agent.automata_actions import Action
from automata.core.agent.automata_agent_helpers import create_builder_from_args
from automata.core.base.openai import OpenAIChatMessage
from automata.evals.eval_helpers import EvalAction, calc_eval_result

logger = logging.getLogger(__name__)


class Eval(abc.ABC):
    """
    Evaluation classes generally should override two methods:
    `generate_eval_result`: Takes an instruction and a list of expected actions and evaluates the correctness of the agent's actions.
    `_extract_actions`: Removes the actions from a passed list of messages.
    """

    def __init__(self, *args, **kwargs):
        if "agent_config" not in kwargs:
            raise ValueError("agent_config must be provided to Eval")
        self.builder = create_builder_from_args(args, kwargs)

    def generate_eval_result(self, instruction: str, expected_actions: List[EvalAction]):
        """
        Evaluates a single sample.
        """
        logger.info("Evaluating Instruction: %s", instruction)
        agent = self.builder.with_instructions(instruction).build()
        agent.run()
        messages = agent.get_non_instruction_messages()
        extracted_actions = Eval._extract_actions(messages)
        return calc_eval_result(extracted_actions, expected_actions)

    @staticmethod
    def _extract_actions(messages: List[OpenAIChatMessage]) -> List[Action]:
        """Extracts actions from a list of messages."""
        extracted_actions: List[Action] = []
        for message in messages:
            actions = AutomataActionExtractor.extract_actions(message.content)
            extracted_actions.extend(actions)
        return extracted_actions
