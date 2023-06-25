from abc import ABC, abstractmethod
from typing import Any, Callable, Optional

from automata.core.base.database.relational import RelationalDatabase
from automata.core.base.observer import Observer


class LLMCompletionResult(ABC):
    """Abstract base class for different types of LLM completion results."""

    @abstractmethod
    def get_content(self) -> Any:
        """Returns the content of the completion result."""
        pass

    @abstractmethod
    def get_function_call(self) -> Any:
        """Returns any function call associated with the completion result."""
        pass


class LLMChatMessage(ABC):
    """Abstract base class for different types of LLM chat messages."""

    def __init__(self, role: str, content: Optional[str] = None) -> None:
        """
        Args:
            role (str): The role of the message.
            content (Optional[str], optional): The content of the message. Defaults to None.
        """
        self.role = role
        self.content = content

    @abstractmethod
    def to_dict(self) -> Any:
        """Returns the message as a dictionary."""
        pass


class LLMConversation(ABC):
    """Abstract base class for different types of LLM conversations."""

    class LLMEmptyConversationError(Exception):
        """Raised when the conversation is empty."""

        def __init__(self, message: str = "The conversation is empty.") -> None:
            super().__init__(message)

    def __init__(self):
        self._observers = set()

    def register_observer(self, observer: Observer):
        self._observers.add(observer)

    def unregister_observer(self, observer: Observer):
        self._observers.discard(observer)

    def notify_observers(self):
        for observer in self._observers:
            observer.update(self)

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


class LLMConversationDatabaseProvider(Observer, ABC):
    """Abstract base class for different types of database providers."""

    def __init__(self, db: RelationalDatabase) -> None:
        self.db = db

    def update(self, subject: LLMConversation):
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
    def get_messages(self, session_id: str) -> None:
        """
        Get all messages of a specific agent.

        Args:
            agent_id (str): The ID of the agent.
        """
        pass

    @abstractmethod
    def replay_messages(self, session_id: str) -> None:
        """
        Replay all messages of a specific agent.

        Args:
            agent_id (str): The ID of the agent.
        """
        pass


class LLMChatProvider(ABC):
    def __init__(self):
        pass

    def get_response(self) -> LLMCompletionResult:
        """
        Returns the latest response from the LLM.

        Args:
            conversation (LLMConversation): The conversation to get the response for.
        """
        raise NotImplementedError
