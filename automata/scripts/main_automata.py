import argparse
import logging
import logging.config
from typing import Dict

from termcolor import colored

from automata.configs.agent_configs import AutomataConfigVersion
from automata.core import Toolkit, ToolkitType, load_llm_toolkits
from automata.core.agents.automata_agent import AutomataAgentBuilder, AutomataAgentConfig
from automata.core.utils import get_logging_config, root_py_path
from automata.tools.python_tools.python_indexer import PythonIndexer


def main():
    logging_config = get_logging_config()
    logging.config.dictConfig(logging_config)
    logger = logging.getLogger(__name__)

    parser = argparse.ArgumentParser(description="Run the AutomataAgent.")
    parser.add_argument("--instructions", type=str, help="The initial instructions for the agent.")
    parser.add_argument(
        "--config_version",
        type=AutomataConfigVersion,
        default=AutomataConfigVersion.AUTOMATA_MASTER_V3,
        help="The config version of the agent.",
    )
    parser.add_argument(
        "--model", type=str, default="gpt-4", help="The model to be used for the agent."
    )
    parser.add_argument(
        "--documentation_url",
        type=str,
        default="https://python.langchain.com/en/latest",
        help="The model to be used for the agent.",
    )
    parser.add_argument(
        "--session_id", type=str, default=None, help="The session id for the agent."
    )
    parser.add_argument(
        "--stream", type=bool, default=True, help="Should we stream the responses?"
    )
    parser.add_argument(
        "--toolkits",
        type=str,
        default="python_indexer,python_writer,codebase_oracle",
        help="Comma-separated list of toolkits to be used.",
    )
    parser.add_argument(
        "--include_overview",
        type=bool,
        default=False,
        help="Should the instruction prompt include an overview?",
    )

    parser.add_argument("-v", "--verbose", action="store_true", help="increase output verbosity")

    args = parser.parse_args()

    logging_config = get_logging_config(log_level=logging.DEBUG if args.verbose else logging.INFO)
    logging.config.dictConfig(logging_config)
    logger = logging.getLogger(__name__)

    requests_logger = logging.getLogger("urllib3")

    # Set the logging level for the requests logger to WARNING
    requests_logger.setLevel(logging.INFO)
    openai_logger = logging.getLogger("openai")
    openai_logger.setLevel(logging.INFO)

    assert not (
        args.instructions is None and args.session_id is None
    ), "You must provide instructions for the agent if you are not providing a session_id."
    assert not (
        args.instructions and args.session_id
    ), "You must provide either instructions for the agent or a session_id."

    inputs = {"documentation_url": args.documentation_url, "model": args.model}
    llm_toolkits: Dict[ToolkitType, Toolkit] = load_llm_toolkits(
        args.toolkits.split(","), **inputs
    )
    if args.include_overview:
        indexer = PythonIndexer(root_py_path())

        initial_payload = {
            "overview": indexer.get_overview(),
        }
    else:
        initial_payload = {}
    logger.info(
        f"Passing in instructions:\n{colored(args.instructions, color='white', on_color='on_green')}"
    )
    logger.info("-" * 60)

    agent_config_version = AutomataConfigVersion(args.config_version)
    agent_config = AutomataAgentConfig.load(agent_config_version)

    agent = (
        AutomataAgentBuilder(agent_config)
        .with_initial_payload(initial_payload)
        .with_instructions(args.instructions)
        .with_llm_toolkits(llm_toolkits)
        .with_model(args.model)
        .with_session_id(args.session_id)
        .with_stream(args.stream)
        .build()
    )

    logger.info("Running the agent now...")
    if args.session_id is None:
        result = agent.run()
        logger.info("Result: %s", result)
    else:
        logger.info("Replaying messages...")
        result = agent.replay_messages()
        logger.info("Result: %s", result)

    while True:
        user_input = input(
            "Do you have any further instructions or feedback? Type 'exit' to terminate: "
        )
        if user_input.lower() == "exit":
            break
        else:
            instructions = [{"role": "user", "content": user_input}]
            agent.modify_last_instruction(instructions)
            agent.iter_task()


if __name__ == "__main__":
    main()
