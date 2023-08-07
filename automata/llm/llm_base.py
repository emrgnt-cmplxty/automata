import json
from abc import ABC, abstractmethod
from typing import (
    Any,
    Dict,
    List,
    NamedTuple,
    Optional,
    Sequence,
    Set,
    Tuple,
    Union,
)

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


class FunctionCall(NamedTuple):
    """A class representing function call to be made by the OpenAI agent."""

    name: str
    arguments: Dict[str, str]

    def to_dict(self) -> Dict[str, Union[Dict[str, str], str]]:
        """Convert the function call to a dictionary."""

        return {
            "name": self.name,
            "arguments": json.dumps(self.arguments),
        }

    @classmethod
    def from_response_dict(
        cls, response_dict: Dict[str, str]
    ) -> "FunctionCall":
        """Create a FunctionCall from a response dictionary."""

        def preprocess_json_string(json_string: str) -> str:
            """Preprocess the JSON string to handle control characters."""
            import re

            # Match only the newline characters that are not preceded by a backslash
            json_string = re.sub(r"(?<!\\)\n", "\\n", json_string)
            # Do the same for tabs or any other control characters
            json_string = re.sub(r"(?<!\\)\t", "\\t", json_string)
            return json_string

        if (
            response_dict["name"] == "call_termination"
            and '"result":' in response_dict["arguments"]
        ):
            return cls(
                name=response_dict["name"],
                arguments=FunctionCall.handle_termination(
                    response_dict["arguments"]
                ),
            )
        try:
            return cls(
                name=response_dict["name"],
                arguments=json.loads(
                    preprocess_json_string(response_dict["arguments"])
                ),
            )
        except Exception as e:
            # TODO - put robust infra sot his bubbles back up to the agent
            return cls(
                name="error-occurred",
                arguments={"error": f"Error occurred: {e}"},
            )

    @staticmethod
    def handle_termination(arguments: str) -> Dict[str, str]:
        """
        Handle the termination message from the conversation.

        Note/FIXME - This is a hacky solution to the problem of parsing Markdown
            with JSON. It needs to be made more robust and generalizable.
            Further, we need to be sure that this is adequate to solve all
            possible problems we might face due to adopting a Markdown return format.
        """

        try:
            return json.loads(arguments)
        except json.decoder.JSONDecodeError as e:
            split_result = arguments.split('{"result":')
            if len(split_result) <= 1:
                raise ValueError(
                    "Invalid arguments for call_termination"
                ) from e
            result_str = split_result[1].strip().replace('"}', "")
            if result_str[0] != '"':
                raise ValueError(
                    "Invalid format for call_termination arguments"
                ) from e
            result_str = result_str[1:]
            return {"result": result_str}

    def __str__(self) -> str:
        return json.dumps(self._asdict())
