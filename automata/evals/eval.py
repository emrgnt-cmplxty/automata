import abc
import logging
from typing import List

from automata.configs.automata_agent_config_utils import AutomataAgentConfigFactory
from automata.core.agent.automata_action_extractor import AutomataActionExtractor
from automata.core.agent.automata_actions import Action
from automata.core.agent.automata_agent import AutomataAgent
from automata.core.agent.automata_agent_utils import AutomataAgentFactory
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
        if "main_config" not in kwargs:
            raise ValueError("main_config must be provided to Eval")
        self.config = AutomataAgentConfigFactory.create_config(args, kwargs)

    def generate_eval_result(self, instructions: str, expected_actions: List[EvalAction]):
        """
        Evaluates a single sample.
        """
        logger.debug("Evaluating Instructions: %s", instructions)
        agent = AutomataAgentFactory.create_agent(instructions=instructions, config=self.config)
        agent.run()
        messages = Eval._extract_non_instruction_messages(agent)
        extracted_actions = Eval._extract_actions(messages)
        return calc_eval_result(extracted_actions, expected_actions)

    @staticmethod
    def _extract_non_instruction_messages(agent: AutomataAgent) -> List[OpenAIChatMessage]:
        """
        Retrieves all messages in the conversation that are not system instructions.

        Returns:
            List[OpenAIChatMessage]: A list of non-instruction messages.
        """
        return agent.messages[agent.NUM_DEFAULT_MESSAGES :]

    @staticmethod
    def _extract_actions(messages: List[OpenAIChatMessage]) -> List[Action]:
        """Extracts actions from a list of messages."""
        extracted_actions: List[Action] = []
        for message in messages:
            actions = AutomataActionExtractor.extract_actions(message.content)
            extracted_actions.extend(actions)
        return extracted_actions
