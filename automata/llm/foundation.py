from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Set, Tuple

from pydantic import BaseModel

from automata.core.base import Observer, SQLDatabase


class LLMCompletionResult(BaseModel):
    """Base class for different types of LLM completion results."""

    role: str
    content: Optional[str] = None

    def get_role(self) -> str:
        return self.role

    def get_content(self) -> Any:
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

        def __init__(self, message: str = "The conversation is empty.") -> None:
            super().__init__(message)

    def __init__(self) -> None:
        self._observers: Set[Observer] = set()

    def register_observer(self, observer: Observer) -> None:
        self._observers.add(observer)

    def unregister_observer(self, observer: Observer) -> None:
        self._observers.discard(observer)

    def notify_observers(self) -> None:
        for observer in self._observers:
            observer.update(self)

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

    def update(self, subject: LLMConversation) -> None:
        """Concrete `Observer` method to update the database when the conversation changes."""
        if isinstance(subject, LLMConversation):
            self.save_message(subject.get_latest_message())

    @abstractmethod
    def save_message(self, message: LLMChatMessage) -> None:
        """An abstract method to save a message to the database."""
        pass

    @abstractmethod
    def get_messages(self) -> List[LLMChatMessage]:
        """An abstract method to get all messages with the original session id."""
        pass


class LLMChatCompletionProvider(ABC):
    """Abstract base class for different types of LLM chat completion providers."""

    @abstractmethod
    def get_next_assistant_completion(self) -> LLMChatMessage:
        """Abstract method to returns the next assistant completion from the LLM."""
        pass

    @abstractmethod
    def add_message(self, message: LLMChatMessage) -> None:
        """Abstract method to add a new message to the provider's buffer."""
        pass

    @abstractmethod
    def reset(self) -> None:
        """Abstract method to reset the chat provider's buffer."""
        pass

    @abstractmethod
    def standalone_call(self, prompt: str) -> str:
        """
        This abstract function enables the utilization of the provider as a unique output LLM.
        For instance, the function exists to permit the user to engage the ChatProvider
        as a sole output supplier, as opposed to a chat provider.


        Throws:
            Exception: If the chat provider's buffer is not devoid of content.
        """
        pass
