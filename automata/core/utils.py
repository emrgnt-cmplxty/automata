import json
import logging
import os
from typing import Any, Dict

import colorlog
import numpy as np
import openai
import yaml
from github import Github
from langchain.chains.conversational_retrieval.base import BaseConversationalRetrievalChain

from automata.config import GITHUB_API_KEY, REPOSITORY_NAME


def format_prompt(format_variables: Dict[str, str], input_text: str) -> str:
    """Format expected strings into the config."""
    for arg in format_variables:
        input_text = input_text.replace(f"{{{arg}}}", format_variables[arg])
    return input_text


def root_py_path() -> str:
    """
    Returns the path to the root of the project python code.

    Returns:
    - A path object in string form

    """
    script_dir = os.path.dirname(os.path.realpath(__file__))
    data_folder = os.path.join(script_dir, "..")
    return data_folder


def load_config(
    config_version: str, file_name: str, config_type: str = "yaml", custom_decoder: Any = None
) -> Any:
    """
    Loads a config file.

    Args:
        file_path (str): The path to the YAML file.

    Returns:
        Any: The content of the YAML file as a Python object.
    """
    with open(
        os.path.join(root_py_path(), "configs", config_version, f"{file_name}.{config_type}"),
        "r",
    ) as file:
        if config_type == "yaml":
            return yaml.safe_load(file)
        elif config_type == "json":
            samples_json_string = file.read()
            return json.loads(samples_json_string, object_hook=custom_decoder)


def root_path() -> str:
    """
    Returns the path to the root of the project directory.

    Returns:
    - A path object in string form

    """
    script_dir = os.path.dirname(os.path.realpath(__file__))
    data_folder = os.path.join(script_dir, "..", "..")
    return data_folder


def get_logging_config(log_level=logging.INFO) -> dict:
    """Returns logging configuration."""
    color_scheme = {
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "bold_red",
    }
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "colored": {
                "()": colorlog.ColoredFormatter,
                "format": "%(log_color)s%(levelname)s:%(name)s:%(message)s",
                "log_colors": color_scheme,
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "colored",
                "level": log_level,
            }
        },
        "root": {"handlers": ["console"], "level": log_level},
    }
    return logging_config


def run_retrieval_chain_with_sources_format(
    chain: BaseConversationalRetrievalChain, q: str
) -> str:
    """Runs a retrieval chain and formats the result with sources.

    Args:
        chain (BaseConversationalRetrievalChain): The retrieval chain to run.
        q (str): The query to pass to the retrieval chain.

    Returns:
        str: The formatted result containing the answer and sources.
    """
    result = chain(q)
    return f"Answer: {result['answer']}.\n\n Sources: {result.get('source_documents', [])}"


def calculate_similarity(content_a: str, content_b: str) -> float:
    """Calculate the similarity between two strings."""
    resp = openai.Embedding.create(
        input=[content_a, content_b], engine="text-similarity-davinci-001"
    )
    embedding_a = resp["data"][0]["embedding"]
    embedding_b = resp["data"][1]["embedding"]
    dot_product = np.dot(embedding_a, embedding_b)
    magnitude_a = np.sqrt(np.dot(embedding_a, embedding_a))
    magnitude_b = np.sqrt(np.dot(embedding_b, embedding_b))
    return dot_product / (magnitude_a * magnitude_b)


def create_issue_on_github(
    title: str,
    body: str,
    labels: list = [],
) -> None:
    """Create an issue on Github."""
    g = Github(GITHUB_API_KEY)
    repo = g.get_repo(REPOSITORY_NAME)
    repo.create_issue(title=title, body=body, labels=labels)
