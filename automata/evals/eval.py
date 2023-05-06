"""
Eval Class

The Eval class provides a base implementation for evaluating an agent's performance when given a set of instructions. The class expects an agent_config to be provided during initialization. Subclasses of Eval should override the eval_sample and run methods to customize evaluation behavior.

Class Methods -

    __init__(self, *args, **kwargs): Initializes an Eval object with the following optional keyword arguments:

    agent_config: Configuration for the AutomataAgentBuilder (required).
    instruction_payload: Instruction payload for the AutomataAgentBuilder.
    model: Model to use for the agent.
    session_id: Session ID for the agent.
    stream: Stream for the agent.
    with_max_iters: Maximum number of iterations for the agent.
    llm_toolkits: Low-level model toolkits for the agent.
    with_master: Option to use the master model.

    generate_eval_result(self, instruction: str, expected_actions: List[EvalAction]) -> EvalResult
    Evaluates a single sample by constructing an agent using the provided instruction, running the agent, extracting the actions performed by the agent, and comparing them to the expected_actions. Returns an EvalResult object with the evaluation results.

    _extract_actions(messages: List[OpenAIChatMessage]) -> List[Action]
    A static method that extracts a list of Action objects from a list of OpenAIChatMessage objects.

Example -

    overview = PythonIndexer(root_py_path()).build_overview()
    agent_messages = AutomataCoordinator().build_agent_message()
    instruction_payload = create_instruction_payload(overview, agent_messages)

    evaluator = Eval(
        agent_config=AutomataAgentConfig.load(AgentConfigVersion.AUTOMATA_INDEXER_DEV),
        llm_toolkits=args.llm_toolkits,
        model=args.model,
        instruction_payload=instruction_payload,
        stream=args.stream,
    )

    eval_result = evaluator.generate_eval_result(instruction, expected_actions)

"""
import abc
import logging
from typing import List

from automata.core.agent.automata_action_extractor import AutomataActionExtractor
from automata.core.agent.automata_actions import Action
from automata.core.agent.automata_agent_builder import create_builder_from_args
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
