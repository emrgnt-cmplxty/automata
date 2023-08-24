import os


def get_root_dir() -> str:
    """Get the path to the root of the Automata python code directory."""

    script_dir = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(script_dir, "..")
