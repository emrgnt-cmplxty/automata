from enum import Enum


class ConfigCategory(Enum):
    """
    ConfigCategory: Enum of agent config categories.
    Corresponds to the folder name which contains yaml configuration files
    """

    SYMBOLS = "symbols"
