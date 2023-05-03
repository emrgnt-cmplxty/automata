"""
This file defines the base class for evals.
"""
import abc
import logging
from typing import Dict, List

from automata.core.agent.automata_action_extractor import AutomataActionExtractor
from automata.core.agent.automata_actions import Action
from automata.core.agent.automata_agent_builder import AutomataAgentBuilder
from automata.evals.eval_helpers import EvalAction, calc_eval_result

logger = logging.getLogger(__name__)


class Eval(abc.ABC):
    """
    Evaluation classes generally should override two methods:
    `eval_sample`: Takes in a test sample and a random number generator and
        records the metrics of interest.
    `run`: Takes in a recorder and runs the evaluation. Generally, most `run`
        methods will follow this same pattern: loading the data, calling
        `eval_all_samples`, and aggregating the recorded results.
    """

    def __init__(self, *args, **kwargs):
        if "agent_config" not in kwargs:
            raise ValueError("agent_config must be provided to Eval")

        self.builder = AutomataAgentBuilder.from_config(kwargs["agent_config"]).with_eval_mode(
            True
        )

        if "instruction_payload" in kwargs and kwargs["instruction_payload"] != {}:
            self.builder = self.builder.with_instruction_payload(kwargs["instruction_payload"])

        if "model" in kwargs:
            self.builder = self.builder.with_model(kwargs["model"])

        if "session_id" in kwargs:
            self.builder = self.builder.with_session_id(kwargs["session_id"])

        if "stream" in kwargs:
            self.builder = self.builder.with_stream(kwargs["stream"])

        if "with_max_iters" in kwargs:
            self.builder = self.builder.with_max_iters(kwargs["with_max_iters"])

        if "with_master" in kwargs:
            self.with_master = kwargs["with_master"]
            if "master_llm_toolkits" in kwargs:
                self.builder = self.builder.with_llm_toolkits(kwargs["master_llm_toolkits"])

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
    def _extract_actions(messages: List[Dict[str, str]]) -> List[Action]:
        extracted_actions: List[Action] = []
        for message in messages:
            actions = AutomataActionExtractor.extract_actions(message["content"])
            extracted_actions.extend(actions)
        return extracted_actions
