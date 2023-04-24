import argparse
import logging
import logging.config
import os
from typing import Optional

from automata.configs.agent_configs import AgentConfig
from automata.core import load_llm_toolkits
from automata.core.agents.automata_agent import AutomataAgent
from automata.core.utils import get_logging_config, root_py_path
from automata.tools.python_tools import PythonIndexer

logger = logging.getLogger(__name__)


def update_docstrings():
    logging.config.dictConfig(get_logging_config())
    parser = argparse.ArgumentParser(description="Run the AutomataAgent.")
    parser.add_argument("--version", type=str, default="automata_docstring_manager_v1")
    parser.add_argument("--file_path", type=Optional[str], default=None)
    args = parser.parse_args()
    llm_toolkits = load_llm_toolkits(["python_indexer", "python_writer"])
    indexer = PythonIndexer(root_py_path())
    if args.file_path:
        pass
    else:
        for module_path in indexer.module_dict:
            if "config" in module_path:
                continue
            if "test" in module_path:
                continue
            if "__init__" in module_path:
                continue
            if "automata_agent" not in module_path:
                continue
            abs_path = os.path.join(root_py_path(), module_path.replace(".", os.sep) + ".py")
            logger.info("Updating documentation and format for %s " % (abs_path))

            with open(abs_path, "r") as file:
                raw_code = file.read()
            logger.info("Initial Code:\n%s" % (raw_code))

            agent = AutomataAgent(
                initial_payload={},
                instructions=f"BEFORE WRITING CODE, begin with a multi-bullet description of what the following file is responsible for:\n {raw_code}"
                f" FOLLOWING that, your objective is to increase the modularity, readability, and maintainability of the file."
                f" BE SURE to include module docstrings, and docstrings for every function, class, method, and function."
                f" You may introduce comments where applicable,"
                f" and rename functions and variables if it significantly improves the code."
                f" NOTE the key changes you have made. The code may be written dirrectly in your prompt and a developer will paste it into the file.",
                llm_toolkits=llm_toolkits,
                version=AgentConfig(args.version),
                model="gpt-4",
                stream=True,
                verbose=True,
            )
            agent.run()

            break
    # for module_path in python_indexer.module

    # (python_indexer, _) = (tool_payload["python_indexer"], tool_payload["python_writer"])
    # overview = python_indexer.get_overview()
    # initial_payload = {"overview": overview}
    # for function in python_parser.function_dict.values():
    #     path = function.py_path
    #     raw_code = python_parser.get_raw_code(path)
    #     docstring = python_parser.get_docstring(path)
    #     if "No results found." not in docstring:
    #         continue
    #     logger.info("Prev Docstring:\n%s" % docstring)
    #     logger.info("Prev Raw Code:\n%s" % raw_code)
    #     instructions = f"The following code is located at the path {path}:\n\n{raw_code}\n\nPlease fetch the code from the raw file, then write relevant docstrings for this piece of code, and lastly, use the python-writer to write the result to disk."
    #     agent = AutomataAgent(
    #         initial_payload=initial_payload,
    #         instructions=instructions,
    #         llm_toolkits=exec_tools,
    #         version=args.version,
    #         model=args.model,
    #         session_id=args.session_id,
    #         stream=args.stream,
    #         verbose=True,
    #     )
    #     agent.run()


if __name__ == "__main__":
    update_docstrings()
