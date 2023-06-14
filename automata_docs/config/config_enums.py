from enum import Enum


class ConfigCategory(Enum):
    """
    An enum which corresponds to the name of a folder holding config
    """

    PROMPT = "prompt"
    SYMBOL = "symbol"
