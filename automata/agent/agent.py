"""Defines the abstract base classes and enums for agent objects"""
import logging
from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Optional, Sequence

import automata.core.utils  # pylint: disable=unused-import
from automata.config import LLMProvider
from automata.llm import (
    LLMChatMessage,
    LLMConversation,
    LLMConversationDatabaseProvider,
    LLMIterationResult,
)
from automata.tools import Tool

logger = logging.getLogger(__name__)


class Agent(ABC):
    """
    An abstract class for implementing a agent.

    An agent is an autonomous entity that can perform actions and communicate
    with other providers.
    """

    def __init__(self, instructions: str) -> None:
        self.instructions = instructions
        self.completed = False
        self.database_provider: Optional[
            LLMConversationDatabaseProvider
        ] = None

        self._initialized = False

    @abstractmethod
    def __iter__(self):
        pass

    @abstractmethod
    def __next__(self) -> LLMIterationResult:
        """
        Iterates the agent by performing a single step of its task.

        A single step is a new conversation turn, which consists of generating
        a new 'asisstant' message, and parsing the reply from the 'user'.

        Raises:
            AgentStopIterationError: If the agent has already completed its task
            or exceeded the maximum number of iterations.
        """
        pass

    @property
    @abstractmethod
    def conversation(self) -> LLMConversation:
        """An abstract property for getting the conversation associated with the agent."""
        pass

    @property
    @abstractmethod
    def agent_responses(self) -> List[LLMChatMessage]:
        """An abstract property for getting the agent responses associated with the agent."""
        pass

    @property
    @abstractmethod
    def tools(self) -> Sequence[Tool]:
        """An abstract property for getting the tools associated with the agent."""
        pass

    @abstractmethod
    def run(self) -> str:
        """
        Runs the agent until it completes its task.

        The task is complete when next returns None.

        Raises:
            AgentError: If the agent has already completed its task or exceeds the maximum number of iterations.
        """
        pass

    @abstractmethod
    def set_database_provider(
        self, provider: LLMConversationDatabaseProvider
    ) -> None:
        """An abstract method for setting the database provider for the agent."""
        pass

    @abstractmethod
    def _setup(self) -> None:
        """An abstract method for setting up the agent before running."""
        pass


class AgentToolkitNames(Enum):
    """
    An enum for the different types of agent tools.

    Each tool type corresponds to a different type of agent tool.
    The associated builders are located in automata/core/agent/builder/*
    """

    # Experimental / Research Tools
    SYMBOL_SEARCH = "symbol-search"
    ADVANCED_CONTEXT_ORACLE = "advanced-context-oracle"
    DOCUMENT_ORACLE = "document-oracle"
    AGENTIFIED_SOLUTION_ORACLE = "agentified-solution-oracle"

    # Core tools
    PY_READER = "py-reader"
    PY_WRITER = "py-writer"
    PY_INTERPRETER = "py-interpreter"
    AGENTIFIED_SEARCH = "agent-search"


class AgentToolkitBuilder(ABC):
    """
    AgentToolkitBuilder is an abstract class for building tools for providers.
    Each builder builds the tools associated with a specific AgentToolkitNames.
    """

    # The tool name, must be included above in `AgentToolkitNames` if set
    TOOL_NAME: Optional[AgentToolkitNames] = None
    LLM_PROVIDER: Optional[LLMProvider] = None

    @abstractmethod
    def build(self) -> List["Tool"]:
        """Builds the tools associated with the `AgentToolkitBuilder`."""
        pass
