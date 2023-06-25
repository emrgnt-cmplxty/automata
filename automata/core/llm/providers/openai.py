import json
import logging
from abc import ABC, abstractmethod
from typing import (
    Any,
    Callable,
    Dict,
    List,
    NamedTuple,
    Optional,
    Sequence,
    Union,
    cast,
)

import numpy as np
import openai

from automata.core.base.agent import Agent, AgentToolBuilder
from automata.core.base.observer import Observer
from automata.core.base.tool import Tool
from automata.core.llm.completion import (
    LLMChatMessage,
    LLMChatProvider,
    LLMCompletionResult,
    LLMConversation,
)
from automata.core.llm.embedding import EmbeddingProvider
from automata.core.utils import set_openai_api_key

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
        self._observers = set()
        self.messages: List[OpenAIChatMessage] = []

    def register_observer(self, observer: Observer):
        self._observers.add(observer)

    def unregister_observer(self, observer: Observer):
        self._observers.discard(observer)

    def notify_observers(self):
        for observer in self._observers:
            observer.update(self)

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


class OpenAIFunction:
    """
    Represents a function callable by the OpenAI agent.
    """

    def __init__(
        self,
        name: str,
        description: str,
        properties: Dict[str, Dict[str, str]],  # TODO - We can probably make this more specific
        required: Optional[List[str]] = None,
    ):
        self.name = name
        self.description = description
        self.properties = properties
        self.required = required or []

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": "object",
                "properties": self.properties,
            },
            "required": self.required,
        }


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
        set_openai_api_key()

    def get_next_assistant_message(self) -> OpenAIChatMessage:
        print("available functions = ", [ele.to_dict() for ele in self.functions])
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=self.conversation.get_messages_for_next_completion(),
            functions=[ele.to_dict() for ele in self.functions],
            function_call="auto",  # auto is default, but we'll be explicit
        )

        return OpenAIChatMessage.from_completion_result(
            OpenAIChatCompletionResult(raw_data=response)
        )


class OpenAIEmbedding(EmbeddingProvider):
    """A class to provide embeddings for symbols"""

    def __init__(self, engine: str = "text-embedding-ada-002") -> None:
        self.engine = engine
        set_openai_api_key()

    def build_embedding(self, symbol_source: str) -> np.ndarray:
        """
        Get the embedding for a symbol.

        Args:
            symbol_source (str): The source code of the symbol

        Returns:
            A numpy array representing the embedding
        """
        # wait to import build_embedding to allow easy mocking of the function in tests.
        from openai.embeddings_utils import get_embedding

        return np.array(get_embedding(symbol_source, engine=self.engine))


class OpenAITool(Tool):
    def __init__(
        self,
        function: Callable[..., str],
        name: str,
        description: str,
        properties: Dict[str, Dict[str, str]],
        required: Optional[List[str]] = None,
        *args: Any,
        **kwargs: Any,
    ):
        super().__init__(function=function, name=name, description=description, **kwargs)
        self.properties = properties
        self.required = required or []
        self.openai_function = self._build_openai_function()

    def _build_openai_function(self) -> OpenAIFunction:
        return OpenAIFunction(
            name=self.name,
            description=self.description,
            properties=self.properties,
            required=self.required,
        )


class OpenAIAgent(Agent):
    def _get_termination_function(self) -> OpenAIFunction:
        return OpenAIFunction(
            name="call_termination",
            description="Terminates the conversation.",
            properties={
                "result": {
                    "type": "string",
                    "description": "The final result of the conversation.",
                }
            },
            required=["result"],
        )

    def _get_available_functions(self) -> Sequence[OpenAIFunction]:
        """

        Gets the available functions for the agent.

        Returns:
            Sequence[OpenAIFunction]: The available functions for the agent.
        """
        raise NotImplementedError


class OpenAIAgentToolBuilder(AgentToolBuilder, ABC):
    """AgentTool is an abstract class for building tools for agents."""

    def __init__(self, **kwargs) -> None:
        pass

    @abstractmethod
    def build(self) -> List[Tool]:
        pass

    @abstractmethod
    def build_for_open_ai(self) -> List[OpenAITool]:
        pass

    @classmethod
    @abstractmethod
    def can_handle(cls, tool_manager: str) -> bool:
        pass
