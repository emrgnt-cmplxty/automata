import logging
import logging.config
import os
from typing import Any, Dict, Tuple

import jsonpickle

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
