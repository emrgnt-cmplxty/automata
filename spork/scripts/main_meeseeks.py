import argparse
import logging
import logging.config

from spork.agents.agent_configs.agent_version import AgentVersion
from spork.agents.mr_meeseeks_agent import MrMeeseeksAgent
from spork.tools.documentation_tools.documentation_gpt import DocumentationGPT
from spork.tools.oracle.codebase_oracle import CodebaseOracle
from spork.tools.python_tools import PythonParser, PythonWriter
from spork.tools.tool_managers import (
    CodebaseOracleToolManager,
    DocumentationGPTToolManager,
    PythonParserToolManager,
    PythonWriterToolManager,
    build_tools,
)
from spork.tools.utils import get_logging_config


def main():
    parser = argparse.ArgumentParser(description="Run the MrMeeseeksAgent.")
    parser.add_argument("--instructions", type=str, help="The initial instructions for the agent.")
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
        "--tools",
        type=str,
        default="python_parser,python_writer,codebase_oracle",
        help="Comma-separated list of tools to be used.",
    )

    logging_config = get_logging_config()
    logging.config.dictConfig(logging_config)
    logger = logging.getLogger(__name__)

    args = parser.parse_args()

    python_parser = PythonParser()
    python_writer = PythonWriter(python_parser)

    exec_tools = []
    if args.tools:
        for tool_name in args.tools.split(","):
            tool_name = tool_name.strip()
            if tool_name.lower() == "python_parser":
                exec_tools += build_tools(PythonParserToolManager(python_parser))
            elif tool_name.lower() == "python_writer":
                exec_tools += build_tools(PythonWriterToolManager(python_writer))
            elif tool_name.lower() == "codebase_oracle":
                codebase_oracle = CodebaseOracle.get_default_codebase_oracle()
                exec_tools += build_tools(CodebaseOracleToolManager(codebase_oracle))
            elif tool_name.lower() == "documentation_gpt":
                doc_gpt = DocumentationGPT(
                    url=args.documentation_url,
                    model=args.model,
                    temperature=0.7,
                    verbose=True,
                )
                exec_tools += build_tools(DocumentationGPTToolManager(doc_gpt))
            else:
                logger.warning("Unknown tool: %s", tool_name)

    overview = python_parser.get_overview()

    initial_payload = {
        "overview": overview,
    }

    logger.info("Passing in instructions: %s", args.instructions)
    logger.info("-" * 100)
    agent = MrMeeseeksAgent(
        initial_payload=initial_payload,
        instructions=args.instructions,
        tools=exec_tools,
        version=args.version,
        model=args.model,
        session_id=args.session_id,
        stream=args.stream,
    )

    logger.info("Running the agent now...")
    if args.session_id is None:
        agent.run()
    else:
        agent.replay_messages()

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
