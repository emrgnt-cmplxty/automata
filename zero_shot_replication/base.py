"""Base classes and enums for zero-shot replication problems."""
from enum import Enum


class ProblemType(Enum):
    """Type of problem to generate"""

    HUMAN_EVAL = "human-eval"
