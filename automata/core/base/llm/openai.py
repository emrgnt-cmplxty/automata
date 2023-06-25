import json
import logging
from typing import Any, Dict, List, NamedTuple, Optional, Union, cast

import openai

from automata.core.base.database.relational import RelationalDatabase
from automata.core.base.llm.llm_types import (
    LLMChatMessage,
    LLMChatProvider,
    LLMCompletionResult,
    LLMConversation,
)

logger = logging.getLogger(__name__)


class FunctionCall(NamedTuple):
    name: str
    arguments: Dict[str, str]

    def to_dict(self) -> Dict[str, Union[Dict[str, str], str]]:
        return {
            "name": self.name,
            "arguments": json.dumps(self.arguments),
        }

    @classmethod
    def from_response_dict(cls, response_dict) -> "FunctionCall":
        return cls(
            name=response_dict["name"],
            arguments=json.loads(response_dict["arguments"]),
        )


class OpenAIBaseCompletionResult(LLMCompletionResult):
    def __init__(self, raw_data: Any) -> None:
        self.raw_data = raw_data

    def get_content(self) -> Optional[str]:
        raise NotImplementedError

    def get_function_call(self) -> Optional[FunctionCall]:
        raise NotImplementedError


class OpenAIChatCompletionResult(OpenAIBaseCompletionResult):
    def get_content(self) -> Optional[str]:
        return self.raw_data["choices"][0]["message"]["content"]

    def get_function_call(self) -> Optional[FunctionCall]:
        result = self.raw_data["choices"][0]["message"]["function_call"]
        return FunctionCall.from_response_dict(result) if result is not None else None


class OpenAIChatMessage(LLMChatMessage):
    def __init__(
        self,
        role: str,
        content: Optional[str] = None,
        function_call: Optional[FunctionCall] = None,
    ) -> None:
        super().__init__(role=role, content=content)
        self.function_call = function_call

    def to_dict(self) -> Dict[str, Any]:
        if self.function_call is None:
            return {"role": self.role, "content": self.content, "function_call": None}

        return {
            "role": self.role,
            "content": self.content,
            "function_call": self.function_call.to_dict(),
        }


class OpenAIIncorrectMessageTypeError(Exception):
    def __init__(self, message: Any) -> None:
        super().__init__(
            f"Expected message to be of type OpenAIChatMessage, but got {type(message)}"
        )


class OpenAIConversation(LLMConversation):
    def __init__(self):
        self.messages: List[OpenAIChatMessage] = []

    def add_message(self, message: LLMChatMessage) -> None:
        if not isinstance(message, OpenAIChatMessage):
            raise OpenAIIncorrectMessageTypeError(message)
        self.messages.append(message)

    def get_messages_for_next_completion(self) -> List[Dict[str, Any]]:
        return [message.to_dict() for message in self.messages]


class OpenAIChatProvider(LLMChatProvider):
    def __init__(self, model: str, temperature: float, stream: bool) -> None:
        self.model = model
        self.temperature = temperature
        self.conversation = OpenAIConversation()
        self.stream = stream

    def get_completion(self, stream: bool) -> OpenAIChatCompletionResult:
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=self.conversation.get_messages_for_next_completion(),
            temperature=self.temperature,
            stream=self.stream,
        )

        completion_response = OpenAIChatCompletionResult(raw_data=response)

        self.conversation.add_message(
            OpenAIChatMessage(
                role="assistant",
                content=completion_response.get_content(),
                function_call=completion_response.get_function_call(),
            )
        )

        return completion_response
