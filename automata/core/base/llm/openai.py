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

    def get_role(self) -> Optional[str]:
        raise NotImplementedError

    def get_content(self) -> Optional[str]:
        raise NotImplementedError

    def get_function_call(self) -> Optional[FunctionCall]:
        raise NotImplementedError


class OpenAIChatCompletionResult(OpenAIBaseCompletionResult):
    def get_role(self) -> str:
        return self.raw_data["choices"][0]["message"]["role"]

    def get_content(self) -> Optional[str]:
        return self.raw_data["choices"][0]["message"]["content"]

    def get_function_call(self) -> Optional[FunctionCall]:
        raw_message = self.raw_data["choices"][0]["message"]
        if "function_call" not in raw_message:
            return None
        elif isinstance(raw_message["function_call"], FunctionCall):
            return raw_message["function_call"]
        else:
            return FunctionCall.from_response_dict(raw_message["function_call"])

    @classmethod
    def from_args(
        cls, role: str, content: str, function_call: Optional[FunctionCall] = None
    ) -> "OpenAIChatCompletionResult":
        return cls(
            raw_data={
                "choices": [
                    {"message": {"role": role, "content": content, "function_call": function_call}}
                ]
            }
        )


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
            return {"role": self.role, "content": self.content}

        return {
            "role": self.role,
            "content": self.content,
            "function_call": self.function_call.to_dict(),
        }

    @classmethod
    def from_completion_result(
        cls, completion_result: OpenAIChatCompletionResult
    ) -> "OpenAIChatMessage":
        """Get an OpenAIChatMessage from an OpenAIChatCompletionResult."""
        return cls(
            role=completion_result.get_role(),
            content=completion_result.get_content(),
            function_call=completion_result.get_function_call(),
        )


class OpenAIIncorrectMessageTypeError(Exception):
    def __init__(self, message: Any) -> None:
        super().__init__(
            f"Expected message to be of type OpenAIChatMessage, but got {type(message)}"
        )


class OpenAIConversation(LLMConversation):
    def __init__(self):
        self.messages: List[OpenAIChatMessage] = []

    def __len__(self) -> int:
        return len(self.messages)

    def add_message(self, message: LLMChatMessage) -> None:
        if not isinstance(message, OpenAIChatMessage):
            raise OpenAIIncorrectMessageTypeError(message)
        self.messages.append(message)

    def add_messages(self, messages: List[LLMChatMessage]) -> None:
        for message in messages:
            self.add_message(message)

    def get_messages_for_next_completion(self) -> List[Dict[str, Any]]:
        return [message.to_dict() for message in self.messages]

    def get_latest_message(self) -> LLMChatMessage:
        return self.messages[-1]


# TODO - Specify this more precisely
OpenAIFunction = Dict[str, Any]


class OpenAIChatProvider(LLMChatProvider):
    def __init__(
        self,
        model: str,
        temperature: float,
        stream: bool,
        functions: List[OpenAIFunction],
        conversation: OpenAIConversation,
    ) -> None:
        self.model = model
        self.temperature = temperature
        self.stream = stream
        self.functions = functions
        self.conversation = conversation

    def get_next_assistant_message(self) -> OpenAIChatMessage:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=self.conversation.get_messages_for_next_completion(),
            # messages=messages,
            functions=self.functions,
            function_call="auto",  # auto is default, but we'll be explicit
        )

        return OpenAIChatMessage.from_completion_result(
            OpenAIChatCompletionResult(raw_data=response)
        )
