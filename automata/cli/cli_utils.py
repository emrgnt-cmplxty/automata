"""
This module contains utility functions for the CLI.
"""

import logging
import os
import shutil
from typing import Any, List, Optional

from questionary import Style, prompt

from automata.core.utils import get_root_fpath
from automata.singletons.py_module_loader import py_module_loader

logger = logging.getLogger(__name__)


def initialize_py_module_loader(
    *args: Any,
    project_root_fpath: Optional[str] = None,
    project_name: Optional[str] = None,
    project_project_name: Optional[str] = None
) -> None:
    """Initializes the py_module_loader with the specified project name and root file path."""

    root_path = project_root_fpath or get_root_fpath()
    project_name = project_project_name or project_name or "automata"
    py_module_loader.initialize(root_path, project_name)


def setup_files(scripts_path: str, dotenv_path: str) -> None:
    """Setup the files necessary for the local task_environment."""

    if not os.path.exists(os.path.join(scripts_path, "setup.sh")):
        try:
            logger.info("Copying setup.sh")
            shutil.copy(
                os.path.join(scripts_path, ".setup.sh.example"),
                os.path.join(scripts_path, "setup.sh"),
            )
        except FileNotFoundError as e:
            raise FileNotFoundError(
                "File .setup.sh.example not found in the scripts path"
            ) from e

    if not os.path.exists(dotenv_path):
        try:
            logger.info("Copying .env")
            shutil.copy(".env.example", dotenv_path)
        except FileNotFoundError as exc:
            raise FileNotFoundError(
                "File .env.example not found in the project root path"
            ) from exc

    # Allow for execution
    os.chmod(os.path.join(scripts_path, "setup.sh"), 0o700)


def get_custom_style() -> Style:
    """Gets the custom style for logging."""

    return Style(
        [
            ("questionmark", "#D65851 bold"),
            ("selected", "#D65851 bold"),
            ("pointer", "#D65851 bold"),
        ]
    )


def ask_choice(message: str, choices: List[str]) -> str:
    """Asks the user for a specific choice."""
    questions = [
        {
            "type": "list",
            "name": "choice",
            "message": message,
            "choices": choices,
        }
    ]

    answers = prompt(questions, style=get_custom_style())
    return answers["choice"]
