import argparse
import logging
import logging.config
import os
from typing import Optional

from automata.configs.agent_configs.config_type import AutomataAgentConfig, AutomataConfigVersion
from automata.core.agents.automata_agent import AutomataAgentBuilder
from automata.core.utils import get_logging_config, root_py_path
from automata.tool_management.tool_management_utils import build_llm_toolkits
from automata.tools.python_tools.python_indexer import PythonIndexer

logger = logging.getLogger(__name__)


def update_docstrings():
    logging.config.dictConfig(get_logging_config())
    parser = argparse.ArgumentParser(description="Run the AutomataAgent.")
    parser.add_argument("--config_version", type=str, default="automata_docstring_manager_v1")
    parser.add_argument("--file_path", type=Optional[str], default=None)
    args = parser.parse_args()
    llm_toolkits = build_llm_toolkits(["python_indexer", "python_writer"])
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

            agent_config_version = AutomataConfigVersion(args.config_version)
            agent_config = AutomataAgentConfig.load(agent_config_version)

            agent = (
                AutomataAgentBuilder(agent_config)
                .with_instructions(
                    f"BEFORE WRITING CODE, begin with a multi-bullet description of what the following file is responsible for:\n {raw_code}"
                    f" FOLLOWING that, your objective is to increase the modularity, readability, and maintainability of the file."
                    f" BE SURE to include module docstrings, and docstrings for every function, class, method, and function."
                    f" You may introduce comments where applicable,"
                    f" and rename functions and variables if it significantly improves the code."
                    f" NOTE the key changes you have made. The code may be written dirrectly in your prompt and a developer will paste it into the file."
                )
                .with_llm_toolkits(llm_toolkits)
                .with_stream(True)
                .with_verbose(True)
                .build()
            )
            agent.run()

            break


if __name__ == "__main__":
    update_docstrings()
