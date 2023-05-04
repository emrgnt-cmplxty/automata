import logging
import logging.config
from typing import Dict, List, Union

from automata.configs.automata_agent_configs import AutomataAgentConfig
from automata.configs.config_enums import AgentConfigVersion
from automata.core.agent.automata_actions import ResultAction, ToolAction
from automata.core.agent.automata_agent_helpers import create_instruction_payload
from automata.core.coordinator.automata_coordinator import AutomataCoordinator
from automata.core.utils import load_config, root_py_path
from automata.evals.eval import Eval
from automata.evals.eval_helpers import EvalAction, EvalResult
from automata.tools.python_tools.python_indexer import PythonIndexer

logger = logging.getLogger(__name__)


def evaluator_decoder(
    dct: Dict[str, Union[str, List[str]]]
) -> Union[EvalAction, Dict[str, Union[str, List[str]]]]:
    if "tool_name" in dct:
        return EvalAction(
            ToolAction(dct["tool_name"], dct["tool_query"], dct["tool_args"]), dct["check_tokens"]  # type: ignore
        )
    elif "result_name" in dct:
        return EvalAction(
            ResultAction(dct["result_name"], dct["result_outputs"]), dct["check_tokens"]  # type: ignore
        )
    return dct


def main(args):
    samples = load_config("eval_configs", "python_indexer_payload", "json", evaluator_decoder)
    eval_results = []
    for sample in samples:
        instruction = sample["instruction"]
        expected_actions = sample["expected_actions"]

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

        try:
            eval_result = evaluator.generate_eval_result(instruction, expected_actions)
            print("EvalResult = ", eval_result)
            eval_results.append(eval_result)
        except Exception as e:
            logger.exception(f"Error {e} when generating eval result.")
            eval_results.append(EvalResult(token_match=False, full_match=False))
