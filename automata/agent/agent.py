"""Defines the abstract base classes and enums for agent objects"""
import logging
import logging.config
from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Optional, Sequence

from automata.config import LLMProvider
from automata.core.utils import get_logging_config
from automata.llm import LLMChatMessage, LLMConversation, LLMIterationResult
from automata.tools import Tool

logger = logging.getLogger(__name__)
logging.config.dictConfig(get_logging_config())


class Agent(ABC):
    """
    An abstract class for implementing a agent.

    An agent is an autonomous entity that can perform actions and communicate
    with other providers.
    """

    def __init__(self, user_instructions: str) -> None:
        self.user_instructions = user_instructions
        self.completed = False

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
    def _setup(self) -> None:
        """An abstract method for setting up the agent before running."""
        pass


class AgentToolkitNames(Enum):
    """
    An enum for the different types of agent tools.

    Each tool type corresponds to a different type of agent tool.
    The associated builders are located in automata/core/agent/builder/*
    """

    WOLFRAM_ALPHA_ORACLE = "wolfram-alpha-oracle"
    PY_INTERPRETER = "py-interpreter"


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
