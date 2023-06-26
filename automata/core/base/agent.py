import logging
from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from automata.config.config_types import AgentConfigName
from automata.core.base.tool import Tool
from automata.core.llm.completion import (
    LLMConversationDatabaseProvider,
    LLMIterationResult,
)
from automata.core.llm.providers.available import LLMPlatforms

logger = logging.getLogger(__name__)


class Agent(ABC):
    """
    An abstract class for implementing a agent.
    An agent is an autonomous entity that can perform actions and communicate with other agents.
    """

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
            AgentError: If the agent has already completed its task or exceeds the maximum number of iterations.

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


class AgentToolProviders(Enum):
    PY_READER = "py_reader"
    PY_WRITER = "py_writer"
    SYMBOL_SEARCH = "symbol_search"
    CONTEXT_ORACLE = "context_oracle"


class AgentToolBuilder(ABC):
    """AgentToolBuilder is an abstract class for building tools for agents."""

    TOOL_TYPE: Optional[AgentToolProviders] = None
    PLATFORM: Optional[LLMPlatforms] = None

    @abstractmethod
    def build(self) -> List[Tool]:
        pass


class AgentInstance(BaseModel):
    """An abstract class for implementing an agent instance."""

    config_name: AgentConfigName = AgentConfigName.DEFAULT
    description: str = ""
    kwargs: Dict[str, Any] = {}

    class Config:
        arbitrary_types_allowed = True

    @abstractmethod
    def run(self, instructions: str) -> str:
        pass

    @classmethod
    def create(
        cls, config_name: AgentConfigName, description: str = "", **kwargs
    ) -> "AgentInstance":
        return cls(config_name=config_name, description=description, kwargs=kwargs)
