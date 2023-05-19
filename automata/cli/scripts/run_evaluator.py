import logging
import logging.config
from typing import Dict, List, Union

from automata.configs.automata_agent_config_utils import build_agent_message
from automata.configs.automata_agent_configs import AutomataAgentConfig, AutomataInstructionPayload
from automata.configs.config_enums import AgentConfigName, ConfigCategory
from automata.core.agent.automata_actions import ResultAction, ToolAction
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
    samples = load_config(ConfigCategory.EVAL.value, args.eval_config, "json", evaluator_decoder)
    eval_results = []
    for sample in samples:
        instruction = sample["instruction"]
        expected_actions = sample["expected_actions"]

        overview = PythonIndexer.build_overview(root_py_path())
        # TODO - Fix this..
        agent_messages = build_agent_message()
        instruction_payload = AutomataInstructionPayload(
            overview=overview, agents_message=agent_messages
        )

        evaluator = Eval(
            main_config=AutomataAgentConfig.load(AgentConfigName.AUTOMATA_INDEXER_DEV),
            llm_toolkits=args.llm_toolkits,
            model=args.model,
            instruction_payload=instruction_payload,
            stream=args.stream,
        )

        try:
            eval_result = evaluator.generate_eval_result(instruction, expected_actions)
            eval_results.append(eval_result)
        except Exception as e:
            logger.exception(f"Error {e} when generating eval result.")
            eval_results.append(EvalResult(token_match=False, full_match=False))
