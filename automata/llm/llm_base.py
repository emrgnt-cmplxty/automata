from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Sequence, Set, Tuple

from pydantic import BaseModel

from automata.core.base import Observer, SQLDatabase


class LLMCompletionResult(BaseModel):
    """Base class for different types of LLM completion results."""

    role: str
    content: Optional[str] = None

    def get_role(self) -> str:
        """Get the role of the completion result."""
        return self.role

    def get_content(self) -> Any:
        """Get the content of the completion result."""
        return self.content


class LLMChatMessage(BaseModel):
    """Base class for different types of LLM chat messages."""

    role: str
    content: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {"role": self.role, "content": self.content}


LLMIterationResult = Optional[Tuple[LLMChatMessage, LLMChatMessage]]


class LLMConversation(ABC):
    """Abstract base class for different types of LLM conversations."""

    class LLMEmptyConversationError(Exception):
        """Raised when the conversation is empty."""

        def __init__(
            self, message: str = "The conversation is empty."
        ) -> None:
            super().__init__(message)

    def __init__(self) -> None:
        self._observers: Set[Observer] = set()

    @property
    @abstractmethod
    def messages(self) -> Sequence[LLMChatMessage]:
        """Abstract property to get the conversation's messages."""
        pass

    def register_observer(self, observer: Observer) -> None:
        """Register an observer to the conversation."""
        self._observers.add(observer)

    def unregister_observer(self, observer: Observer) -> None:
        """Unregister an observer from the conversation."""
        self._observers.discard(observer)

    def notify_observers(self, session_id: str) -> None:
        """Notify all observers that the conversation has changed."""
        for observer in self._observers:
            observer.update((session_id, self))

    @abstractmethod
    def __len__(self) -> int:
        """Abstract method to get the length of the conversation."""
        pass

    @abstractmethod
    def get_messages_for_next_completion(self) -> Any:
        """Abstract method to get the messages to be used for the next completion."""
        pass

    @abstractmethod
    def get_latest_message(self) -> LLMChatMessage:
        """Abstract method to get the last chat message in the conversation."""
        pass

    @abstractmethod
    def reset_conversation(self) -> None:
        """Abstract method to reset the conversation."""
        pass


class LLMConversationDatabaseProvider(Observer, SQLDatabase, ABC):
    """Abstract base class for different types of database providers."""

    def update(self, subject: Tuple[str, LLMConversation]) -> None:
        """Concrete `Observer` method to update the database when the conversation changes."""
        session_id, message = subject
        if isinstance(message, LLMConversation):
            self.save_message(session_id, message.get_latest_message())

    @abstractmethod
    def save_message(self, session_id: str, message: LLMChatMessage) -> None:
        """An abstract method to save a message to the database."""
        pass

    @abstractmethod
    def get_messages(self, session_id: str) -> List[LLMChatMessage]:
        """An abstract method to get all messages with the original session id."""
        pass


class LLMChatCompletionProvider(ABC):
    """Abstract base class for different types of LLM chat completion providers."""

    @abstractmethod
    def get_next_assistant_completion(self) -> LLMChatMessage:
        """Abstract method to returns the next assistant completion from the LLM."""
        pass

    @abstractmethod
    def add_message(
        self, message: LLMChatMessage, session_id: Optional[str] = None
    ) -> None:
        """Abstract method to add a new message to the provider's buffer."""
        pass

    @abstractmethod
    def reset(self) -> None:
        """Abstract method to reset the chat provider's buffer."""
        pass

    @abstractmethod
    def standalone_call(
        self, prompt: str, session_id: Optional[str] = None
    ) -> str:
        """
        This abstract function enables the utilization of the provider as a unique output LLM.
        For instance, the function exists to permit the user to engage the ChatProvider
        as a sole output supplier, as opposed to a chat provider.


        Throws:
            Exception: If the chat provider's buffer is not devoid of content.
        """
        pass
