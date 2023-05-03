import logging
import logging.config
from typing import Dict, List, Union

from automata.configs.automata_agent_configs import AutomataAgentConfig
from automata.configs.config_enums import AgentConfigVersion
from automata.core.agent.automata_actions import ResultAction, ToolAction
from automata.core.agent.automata_agent_helpers import create_instruction_payload
from automata.core.coordinator.automata_coordinator import AutomataCoordinator
from automata.core.utils import root_py_path
from automata.evals.eval import Eval
from automata.evals.eval_helpers import EvalAction
from automata.tools.python_tools.python_indexer import PythonIndexer

logger = logging.getLogger(__name__)


samples: List[Dict[str, Union[str, List[EvalAction]]]] = [
    {
        "instruction": "Query the indexer agent for the class AutomataAgent's method 'run' and return the raw code code",
        "expected_actions": [
            EvalAction(
                ToolAction(
                    "python-indexer-retrieve-raw-code",
                    "tool_query_1",
                    ["core.agent.automata_agent", "AutomataAgent.run"],
                ),
                ["core.agent.automata_agent", "AutomataAgent.run"],
            ),
            EvalAction(
                ResultAction(
                    "return_result_0",
                    [
                        "The raw code for the 'run' method of the AutomataAgent class is: {tool_output_1}"
                    ],
                ),
                ["{tool_output_1}"],
            ),
        ],
    },
]


def main(args):
    instruction = samples[0]["instruction"]
    expected_actions = samples[0]["expected_actions"]

    agent_messages = AutomataCoordinator().build_agent_message()
    overview = PythonIndexer(root_py_path()).build_overview()
    instruction_payload = create_instruction_payload(overview, agent_messages)
    evaluator = Eval(
        agent_config=AutomataAgentConfig.load(AgentConfigVersion.AUTOMATA_INDEXER_DEV),
        master_llm_toolkits=args.master_toolkits,
        model=args.model,
        instruction_payload=instruction_payload,
        stream=True,
    )

    generate_eval_result = evaluator.generate_eval_result(instruction, expected_actions)
    logger.info("generate_eval_result = ", generate_eval_result)
