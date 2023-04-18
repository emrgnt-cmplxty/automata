import argparse
import logging

from spork.tools.agents.agent_configs.agent_version import AgentVersion
from spork.tools.agents.agent_mr_meeseeks import AgentMrMeeseeks
from spork.tools.python_tools import PythonParser, PythonWriter
from spork.tools.tool_managers import PythonParserToolManager, PythonWriterToolManager, build_tools

logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description="Run the AgentMrMeeseeks.")
    parser.add_argument(
        "--initial_instructions", type=str, help="The initial instructions for the agent."
    )
    parser.add_argument(
        "--version",
        type=AgentVersion,
        default=AgentVersion.MEESEEKS_V1,
        help="The version of the agent.",
    )
    parser.add_argument(
        "--model", type=str, default="gpt-4", help="The model to be used for the agent."
    )
    parser.add_argument(
        "--session_id", type=str, default=None, help="The session id for the agent."
    )
    parser.add_argument("--stream", type=str, default=True, help="Should we stream the responses?")

    args = parser.parse_args()

    python_parser = PythonParser()
    python_writer = PythonWriter(python_parser)

    exec_tools = []
    exec_tools += build_tools(PythonParserToolManager(python_parser))
    exec_tools += build_tools(PythonWriterToolManager(python_writer))
    overview = python_parser.get_overview()

    initial_payload = {
        "overview": overview,
    }

    logger.info("Passing in initial_instructions: %s", args.initial_instructions)
    agent = AgentMrMeeseeks(
        initial_payload=initial_payload,
        instructions=args.initial_instructions,
        tools=exec_tools,
        version=args.version,
        model=args.model,
        session_id=args.session_id,
        stream=args.stream,
    )

    logger.info("Running the agent now...")
    agent.run()

    while True:
        user_input = input(
            "Do you have any further instructions or feedback? Type 'exit' to terminate: "
        )
        if user_input.lower() == "exit":
            break
        else:
            instructions = [{"role": "user", "content": user_input}]
            agent.iter_task(instructions)


if __name__ == "__main__":
    main()
