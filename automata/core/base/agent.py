import logging
from abc import ABC, abstractmethod
from typing import Any, List, Optional, Tuple

from automata.core.base.tool import Tool
from automata.core.llm.completion import (
    LLMCompletionResult,
    LLMConversationDatabaseProvider,
    LLMIterationResult,
)
from automata.core.llm.providers.available import AgentToolProviders, LLMPlatforms

logger = logging.getLogger(__name__)


class Agent(ABC):
    """
    An abstract class for implementing a agent.
    An agent is an autonomous entity that can perform actions and communicate with other agents.
    """

    class MaxIterError(Exception):
        """An exception raised when the agent exceeds the maximum number of iterations."""

        pass

    def __init__(self, instructions: str) -> None:
        """
        Args:
            instructions (str): The instructions to be executed by the agent.
            config (Any): The configuration for the agent.
        """
        self.instructions = instructions
        self.completed = False
        self.database_provider: Optional[LLMConversationDatabaseProvider] = None

    @abstractmethod
    def __iter__(self):
        pass

    @abstractmethod
    def __next__(self) -> LLMIterationResult:
        """
        Iterates the agent by performing a single step of its task.
        A single step is a new conversation turn, which consists of generating
        a new 'asisstant' message, and parsing the reply from the 'user'.

        Returns:
            Optional[Tuple[LLMCompletionResult, LLMCompletionResult]]:
                The latest assistant and user messages, or None if the task is completed.
        """
        pass

    @abstractmethod
    def run(self) -> str:
        """
        Runs the agent until it completes its task.
        The task is complete when iter_step returns None.

        Raises:
            ValueError: If the agent has already completed its task.
            MaxIterError: If the agent exceeds the maximum number of iterations.

        Note: The agent must be setup before running.
        """
        pass

    @abstractmethod
    def set_database_provider(self, provider: LLMConversationDatabaseProvider) -> None:
        """
        Sets the database provider for the agent.

        Args:
            provider (LLMConversationDatabaseProvider): The database provider.
        """
        pass

    @abstractmethod
    def _setup(self) -> None:
        """Sets up the agent before running."""
        pass


class AgentToolBuilder(ABC):
    """AgentToolBuilder is an abstract class for building tools for agents."""

    TOOL_TYPE: Optional[AgentToolProviders] = None
    PLATFORM: Optional[LLMPlatforms] = None

    def __init__(self, **kwargs) -> None:
        pass

    @abstractmethod
    def build(self) -> List[Tool]:
        pass
