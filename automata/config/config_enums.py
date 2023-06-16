from enum import Enum


class ConfigCategory(Enum):
    """
    A class to represent the different categories of configuration options
    """

    PROMPT = "prompt"
    SYMBOL = "symbol"
