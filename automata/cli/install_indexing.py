"""
This script instealls indexing and generates local indices directly from the CLI.
"""

import logging
import os
import pathlib
import shutil
import subprocess
from typing import List

logger = logging.getLogger(__name__)


def get_project_paths() -> tuple[str, str, str, str, str, str]:
    """
    Defines the paths used for the project and returns them as a tuple.
    """
    # Directory of the script being executed
    script_dir = pathlib.Path(__file__).parent.absolute()

    # Root directory of the Automata project
    automata_root = script_dir.parent.parent

    # Relative path from the Automata root to the directory where embedding data is stored
    embedding_data_path = os.path.relpath(
        os.path.join(automata_root, "automata-embedding-data"), automata_root
    )

    # Relative path from the Automata root to the factory directory
    factory_path = os.path.relpath(
        os.path.join(automata_root, "automata_embedding_factory"),
        automata_root,
    )

    # Name of the project
    project_name = "automata"

    # Directory path to the SCIP Python project
    scip_python_path = os.path.join(automata_root, "scip-python")

    # Directory path to the project within the factory
    project_in_factory = os.path.join(factory_path, project_name)

    return (
        str(automata_root),
        embedding_data_path,
        factory_path,
        project_name,
        scip_python_path,
        project_in_factory,
    )


def git(*args) -> int:
    """Executes git [args] in the local environtment"""
    return subprocess.check_call(["git"] + list(args))


def install_indexing() -> None:
    """Attempts to execute the install indexing script"""
    (
        automata_root,
        _,
        _,
        _,
        scip_python_path,
        _,
    ) = get_project_paths()

    try:
        os.chdir(scip_python_path)
        subprocess.run(["npm", "install"], check=True)

        os.chdir(os.path.join(scip_python_path, "packages/pyright-scip"))
        subprocess.run(["npm", "run", "build"], check=True)
    except Exception as e:
        logger.error(f"Failed to install indexing: {str(e)}")
        raise
    finally:
        os.chdir(automata_root)


def generate_local_indices() -> None:
    """Generates the local project indices"""
    (
        automata_root,
        embedding_data_path,
        factory_path,
        project_name,
        scip_python_path,
        project_in_factory,
    ) = get_project_paths()

    project_indices = os.path.join(
        embedding_data_path, "indices", f"{project_name}.scip"
    )

    # Remove the old index if it exists
    if os.path.exists(project_indices):
        os.remove(project_indices)

    if os.path.exists(factory_path):
        shutil.rmtree(factory_path)
    os.makedirs(factory_path)

    def ignore_dirs(src: str, names: list[str]) -> list[str]:
        ignored_dirs = ["automata_embedding_factory", "scip-python"]
        return [name for name in names if name in ignored_dirs]

    shutil.copytree(automata_root, project_in_factory, ignore=ignore_dirs)

    commands = install_nvm_and_nodejs("16.10.0")

    node_command = " ".join(
        [
            "node",
            os.path.join(
                scip_python_path, "packages", "pyright-scip", "index"
            ),
            "index",
            "--project-name",
            project_name,
            "--output",
            "automata-embedding-data/indices/automata.scip",
            "--target-only",
            project_name,
        ]
    )

    logger.info(f"Running: {node_command}")

    commands.append(node_command)
    command_string = " && ".join(commands)

    subprocess.run(command_string, check=True, shell=True)


def install_nvm_and_nodejs(version: str) -> List[str]:
    """
    Installs NVM (Node Version Manager) and a specific Node.js version.

    This function expects that you have curl and bash installed on your system.
    """
    # Download and install NVM
    return [
        "curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.38.0/install.sh | bash",
        'export NVM_DIR="$HOME/.nvm"',
        '[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"',
        '[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"',
        f"nvm install {version}",
        f"nvm use {version}",
    ]
