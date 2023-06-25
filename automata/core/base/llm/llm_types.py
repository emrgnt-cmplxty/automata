from abc import ABC, abstractmethod
from typing import Any


class LLMCompletionResult(ABC):
    @abstractmethod
    def get_content(self) -> list[str]:
        pass


class LLMConversation(ABC):
    def __init__(self):
        pass

    def add_message(self, payload: Any) -> None:
        pass

    def get_messages_for_new_completion(self) -> Any:
        pass


class LLMChatProvider(ABC):
    def __init__(self):
        pass

    def get_response(self, conversation: LLMConversation) -> LLMCompletionResult:
        raise NotImplementedError
