import os
import shutil

from questionary import Style, prompt

from automata.core.utils import get_root_fpath
from automata.singletons.py_module_loader import py_module_loader


def initialize_modules(*args, **kwargs) -> None:
    root_path = kwargs.get("project_root_fpath") or get_root_fpath()
    project_name = kwargs.get("project_name") or "automata"
    rel_py_path = kwargs.get("project_rel_py_path") or project_name
    py_module_loader.initialize(root_path, rel_py_path)


def setup_files(SCRIPTS_PATH, DOTENV_PATH):
    if not os.path.exists(os.path.join(SCRIPTS_PATH, "setup.sh")):
        try:
            print("Copying setup.sh")
            shutil.copy(
                os.path.join(SCRIPTS_PATH, ".setup.sh.example"),
                os.path.join(SCRIPTS_PATH, "setup.sh"),
            )
        except FileNotFoundError:
            raise FileNotFoundError(
                "File .setup.sh.example not found in the scripts path"
            )

    if not os.path.exists(DOTENV_PATH):
        try:
            print("Copying .env")
            shutil.copy(".env.example", DOTENV_PATH)
        except FileNotFoundError:
            raise FileNotFoundError(
                "File .env.example not found in the project root path"
            )

    # Allow for execution
    os.chmod(os.path.join(SCRIPTS_PATH, "setup.sh"), 0o700)


def get_custom_style():
    return Style(
        [
            ("questionmark", "#D65851 bold"),
            ("selected", "#D65851 bold"),
            ("pointer", "#D65851 bold"),
        ]
    )


def ask_choice(message, choices):
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
