"""This module provides functions to interact with the GitHub API, specifically to list repositories, issues, and pull requests,
choose a work item to work on, and remove HTML tags from text."""
import logging
import os
from typing import Any, Dict, List

import colorlog
import numpy as np
import openai
import yaml
from langchain.chains.conversational_retrieval.base import BaseConversationalRetrievalChain
from langchain.document_loaders import TextLoader
from langchain.schema import Document


def format_config(format_variables: Dict[str, str], input_text: str) -> str:
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


def load_yaml_config(config_type: str, file_name: str) -> Any:
    """
    Loads a YAML config file.

    Args:
        file_path (str): The path to the YAML file.

    Returns:
        Any: The content of the YAML file as a Python object.
    """
    with open(
        os.path.join(root_py_path(), "configs", config_type, f"{file_name}.yaml"),
        "r",
    ) as file:
        return yaml.safe_load(file)


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
    resp = openai.Embedding.create(
        input=[content_a, content_b], engine="text-similarity-davinci-001"
    )
    embedding_a = resp["data"][0]["embedding"]
    embedding_b = resp["data"][1]["embedding"]
    dot_product = np.dot(embedding_a, embedding_b)
    magnitude_a = np.sqrt(np.dot(embedding_a, embedding_a))
    magnitude_b = np.sqrt(np.dot(embedding_b, embedding_b))
    return dot_product / (magnitude_a * magnitude_b)


class NumberedLinesTextLoader(TextLoader):
    def load(self) -> List[Document]:
        """Load from file path."""
        with open(self.file_path, encoding=self.encoding) as f:
            lines = f.readlines()
            text = f"{self.file_path}"
            for i, line in enumerate(lines):
                text += f"{i}: {line}"
        metadata = {"source": self.file_path}
        return [Document(page_content=text, metadata=metadata)]
