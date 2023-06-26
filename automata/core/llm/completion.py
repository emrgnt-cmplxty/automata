from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple

from pydantic import BaseModel

from automata.core.base.database.relational import SQLDatabase
from automata.core.base.observer import Observer


class LLMCompletionResult(BaseModel):
    """Base class for different types of LLM completion results."""

    role: str
    content: Optional[str] = None

    def get_role(self) -> str:
        """Returns the role of the completion result."""
        return self.role

    def get_content(self) -> Any:
        """Returns the content of the completion result."""
        return self.content


class LLMChatMessage(BaseModel):
    """Base class for different types of LLM chat messages."""

    role: str
    content: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Returns the message as a dictionary."""
        return {"role": self.role, "content": self.content}


LLMIterationResult = Optional[Tuple[LLMChatMessage, LLMChatMessage]]


class LLMConversation(ABC):
    """Abstract base class for different types of LLM conversations."""

    class LLMEmptyConversationError(Exception):
        """Raised when the conversation is empty."""

        def __init__(self, message: str = "The conversation is empty.") -> None:
            super().__init__(message)

    @abstractmethod
    def register_observer(self, observer: Observer) -> None:
        """Registers an observer to the conversation."""
        pass

    @abstractmethod
    def unregister_observer(self, observer: Observer) -> None:
        """Unregisters a specified observer to the conversation."""
        pass

    @abstractmethod
    def notify_observers(self):
        """Notifies all observers of the conversation."""
        pass

    @abstractmethod
    def add_message(self, message: LLMChatMessage) -> None:
        """
        Adds a new message to the conversation.

        Args:
            payload (Any): The message payload.
        """
        pass

    @abstractmethod
    def get_messages_for_next_completion(self) -> Any:
        """Returns the messages to be used for the next completion."""
        pass

    @abstractmethod
    def get_latest_message(self) -> LLMChatMessage:
        """Get the last chat message in the conversation.

        Returns:
            LLMChatMessage: The last chat message in the conversation.

        Raises:
            LLMConversation.LLMEmptyConversationError: If the conversation is empty.
        """
        pass

    @abstractmethod
    def reset_conversation(self) -> None:
        """Resets the conversation."""
        pass


class LLMConversationDatabaseProvider(Observer, SQLDatabase, ABC):
    """Abstract base class for different types of database providers."""

    def __init__(self, session_id: str, db_path: str) -> None:
        pass

    def update_database(self, subject: LLMConversation) -> None:
        """
        Update the database when the conversation changes.

        Args:
            subject (LLMConversation): The conversation that changed.
        """
        if isinstance(subject, LLMConversation):
            self.save_message(subject.get_latest_message())

    @abstractmethod
    def save_message(self, message: LLMChatMessage) -> None:
        """
        Save a message to the database.

        Args:
            message (str): The message to save.
            agent_id (str): The ID of the agent.
        """
        pass

    @abstractmethod
    def get_messages(self) -> List[LLMChatMessage]:
        """
        Get all messages of a specific agent.

        Args:
            agent_id (str): The ID of the agent.
        """
        pass


class LLMChatCompletionProvider(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_next_assistant_completion(self) -> LLMChatMessage:
        """
        Returns the next assistant completion from the LLM.
        """
        pass

    @abstractmethod
    def add_message(self, message: LLMChatMessage) -> None:
        """
        Appends a new user message to the chat completion provider
        """
        pass

    @abstractmethod
    def reset(self) -> None:
        """
        Resets the chat provider
        """
        pass
