import argparse
import logging
import logging.config
from typing import Dict

from spork.configs.agent_configs import AgentVersion
from spork.core import Toolkit, ToolkitType, load_llm_toolkits
from spork.core.agents.mr_meeseeks_agent import MrMeeseeksAgent
from spork.core.utils import get_logging_config, root_py_path
from spork.tools.python_tools.python_indexer import PythonIndexer


def main():
    logging_config = get_logging_config()
    logging.config.dictConfig(logging_config)
    logger = logging.getLogger(__name__)

    parser = argparse.ArgumentParser(description="Run the MrMeeseeksAgent.")
    parser.add_argument("--instructions", type=str, help="The initial instructions for the agent.")
    parser.add_argument(
        "--version",
        type=AgentVersion,
        default=AgentVersion.MEESEEKS_MASTER_V1,
        help="The version of the agent.",
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

    args = parser.parse_args()
    assert not (
        args.instructions is None and args.session_id is None
    ), "You must provide instructions for the agent if you are not providing a session_id."
    assert not (
        args.instructions and args.session_id
    ), "You must provide either instructions for the agent or a session_id."

    inputs = {"documentation_url": args.documentation_url, "model": args.model}
    llm_toolkits: Dict[ToolkitType, Toolkit] = load_llm_toolkits(
        args.toolkits.split(","), inputs, logger
    )
    indexer = PythonIndexer(root_py_path())

    initial_payload = {
        "overview": indexer.get_overview(),
    }

    logger.info("Passing in instructions: %s", args.instructions)
    logger.info("-" * 100)
    agent = MrMeeseeksAgent(
        initial_payload=initial_payload,
        instructions=args.instructions,
        llm_toolkits=llm_toolkits,
        version=args.version,
        model=args.model,
        session_id=args.session_id,
        stream=args.stream,
    )

    logger.info("Running the agent now...")
    if args.session_id is None:
        logger.info("Running...")
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
            agent.extend_last_instructions(instructions)
            agent.iter_task()


if __name__ == "__main__":
    main()
