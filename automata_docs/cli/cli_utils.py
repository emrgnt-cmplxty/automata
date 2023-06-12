import logging
import logging.config
import os
from typing import Any, Dict, Tuple

import jsonpickle

from configs.automata_agent_config_utils import AutomataAgentConfigFactory
from configs.automata_agent_configs import AutomataAgentConfig
from configs.config_enums import AgentConfigName, ConfigCategory
from automata_docs.core.code_indexing.utils import build_repository_overview
from automata_docs.core.search.symbol_types import Symbol
from automata_docs.core.utils import config_path, get_logging_config, root_py_path

logger = logging.getLogger(__name__)


def reconfigure_logging(log_level: int):
    """
    Configure the logging settings.

    :param verbose: Boolean, if True, set log level to DEBUG, else set to INFO.
    """
    logging_config = get_logging_config(log_level=log_level)
    logging.config.dictConfig(logging_config)

    # Set the logging level for the requests logger to WARNING
    requests_logger = logging.getLogger("urllib3")
    requests_logger.setLevel(log_level)
    openai_logger = logging.getLogger("openai")
    openai_logger.setLevel(log_level)


def check_kwargs(kwargs):
    assert (
        "helper_agent_names" in kwargs
    ), "You must provide a list of helper agents, with field helper_agent_names."
    assert (
        "main_config_name" in kwargs or "main_config" in kwargs
    ), "You must provide a main agent config name, with field main_config_name."


def create_instructions_and_config_from_kwargs(
    **kwargs,
) -> Tuple[str, AutomataAgentConfig]:
    instructions = kwargs.get("instructions")
    if not isinstance(instructions, str):
        raise ValueError("instructions must be provided")
    del kwargs["instructions"]

    if "main_config" in kwargs:
        return instructions, kwargs["main_config"]

    return instructions, create_config_from_kwargs(**kwargs)


def create_config_from_kwargs(**kwargs) -> AutomataAgentConfig:
    logger.debug(f"Loading helper configs...")
    helper_agent_names = kwargs.get("helper_agent_names")
    if helper_agent_names:
        if not isinstance(helper_agent_names, str):
            raise ValueError("helper_agent_names must be a comma-separated string.")
        helper_agent_configs = {
            AgentConfigName(helper_config_name): AutomataAgentConfigFactory.create_config(
                main_config_name=helper_config_name
            )
            for helper_config_name in helper_agent_names.split(",")
        }
        kwargs["helper_agent_configs"] = helper_agent_configs
        del kwargs["helper_agent_names"]

    logger.debug(f"Loading main agent config..   .")
    kwargs["main_config"] = AutomataAgentConfigFactory.create_config(**kwargs)
    del kwargs["main_config_name"]

    if kwargs.get("include_overview"):
        instruction_payload = kwargs.get("instruction_payload", {})
        instruction_payload["overview"] = build_repository_overview(root_py_path())
        kwargs["instruction_payload"] = instruction_payload

    return AutomataAgentConfigFactory.create_config(None, **kwargs)


def load_docs(kwargs: Dict[str, Any]) -> Dict[Symbol, Tuple[str, str, str, str]]:
    doc_path = os.path.join(
        config_path(),
        ConfigCategory.SYMBOLS.value,
        kwargs.get("documentation_path", "symbol_documentation.json"),
    )

    docs: Dict[Symbol, Tuple[str, str, str, str]] = {}
    if kwargs.get("update_docs"):
        try:
            if not os.path.exists(doc_path):
                raise Exception("No docs to update.")
            with open(doc_path, "r") as file:
                loaded_docs: Dict = jsonpickle.decode(file.read())
                docs = {Symbol.from_string(key): value for key, value in loaded_docs.items()}
        except Exception as e:
            logger.error(f"Failed to load docs: {e}")
    return docs


def save_docs(kwargs: Dict[str, Any], docs: Dict[Symbol, Tuple[str, str, str, str]]):
    doc_path = os.path.join(
        config_path(),
        ConfigCategory.SYMBOLS.value,
        kwargs.get("documentation_path", "symbol_documentation.json"),
    )

    pickle_str = jsonpickle.encode(docs)

    with open(doc_path, "w") as file:
        file.write(pickle_str)
