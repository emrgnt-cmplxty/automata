import json
import logging
from typing import Any, Callable, Dict, List, NamedTuple, Optional, Union

import numpy as np
import openai
import tiktoken
from termcolor import colored

from automata.core.utils import set_openai_api_key
from automata.embedding import EmbeddingVectorProvider
from automata.llm import (
    LLMChatCompletionProvider,
    LLMChatMessage,
    LLMCompletionResult,
    LLMConversation,
)
from automata.tools.base import Tool

logger = logging.getLogger(__name__)


class FunctionCall(NamedTuple):
    """A class representing function call to be made by the OpenAI agent."""

    name: str
    arguments: Dict[str, str]

    def to_dict(self) -> Dict[str, Union[Dict[str, str], str]]:
        return {
            "name": self.name,
            "arguments": json.dumps(self.arguments),
        }

    @classmethod
    def from_response_dict(
        cls, response_dict: Dict[str, str]
    ) -> "FunctionCall":
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
        return cls(
            name=response_dict["name"],
            arguments=json.loads(response_dict["arguments"]),
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


class OpenAIChatCompletionResult(LLMCompletionResult):
    """A class to represent a completion result from the OpenAI API."""

    function_call: Optional[Dict[str, Any]] = None

    def __init__(self, raw_data: Any) -> None:
        raw_message = raw_data["choices"][0]["message"]
        role = raw_message["role"]
        content = raw_message["content"]
        super().__init__(role=role, content=content)
        self.function_call = (
            raw_message["function_call"]
            if "function_call" in raw_message
            else None
        )

    def __str__(self) -> str:
        return f"{self.role}:\ncontent={self.content}\nfunction_call={self.function_call}"

    def get_function_call(self) -> Optional[FunctionCall]:
        if not self.function_call:
            return None
        else:
            return FunctionCall.from_response_dict(self.function_call)

    @classmethod
    def from_args(
        cls,
        role: str,
        content: str,
        function_call: Optional[FunctionCall] = None,
    ) -> "OpenAIChatCompletionResult":
        return cls(
            raw_data={
                "choices": [
                    {
                        "message": {
                            "role": role,
                            "content": content,
                            "function_call": function_call,
                        }
                    }
                ]
            }
        )


class OpenAIChatMessage(LLMChatMessage):
    """A class to represent a processed chat message TO or FROM the OpenAI LLM Chat API."""

    function_call: Optional[FunctionCall] = None

    def __init__(
        self,
        role: str,
        content: Optional[str] = None,
        function_call: Optional[FunctionCall] = None,
    ) -> None:
        super().__init__(role=role, content=content)
        self.function_call = function_call

    def __str__(self) -> str:
        return f"{self.role}:\ncontent={self.content}\nfunction_call={self.function_call}"

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
    """A class to represent a conversation with the OpenAI API."""

    def __init__(self) -> None:
        super().__init__()
        self.messages: List[OpenAIChatMessage] = []

    def __len__(self) -> int:
        return len(self.messages)

    def add_message(self, message: LLMChatMessage) -> None:
        if not isinstance(message, OpenAIChatMessage):
            raise OpenAIIncorrectMessageTypeError(message)
        self.messages.append(message)

    def get_messages_for_next_completion(self) -> List[Dict[str, Any]]:
        return [message.to_dict() for message in self.messages]

    def get_latest_message(self) -> LLMChatMessage:
        return self.messages[-1]

    def reset_conversation(self) -> None:
        self.messages = []


class OpenAIFunction:
    """A class to represent a function callable by the OpenAI agent."""

    def __init__(
        self,
        name: str,
        description: str,
        properties: Dict[
            str, Dict[str, str]
        ],  # TODO - We can probably make this more specific
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

    # prompt format logic taken from Auto-GPT
    # https://github.com/Significant-Gravitas/Auto-GPT/blob/3425b061b5e55b6b655d59d320c8c36895156830/autogpt/llm/providers/openai.py#L359-L408
    @property
    def prompt_format(self) -> str:
        """Returns the function formatted similarly to the way OpenAI does it internally:
        https://community.openai.com/t/how-to-calculate-the-tokens-when-using-function-call/266573/18

        Example:
        ```ts
        // Get the current weather in a given location
        type get_current_weather = (_: {
        // The city and state, e.g. San Francisco, CA
        location: string,
        unit?: "celsius" | "fahrenheit",
        }) => any;
        ```

        ->
        OpenAITool(
            name="call_termination",
            description="Terminates the conversation.",
            properties={
                "result": {
                    "type": "string",
                    "description": "The final result of the conversation.",
                }
            },
            required=["result"],
            function=terminate,
        ).prompt_format
        ==

        ```ts
        // Terminates the conversation.
        type call_termination = (_: {
        // The final result of the conversation.
        result: string,
        }) => any;
        ```

        """

        def param_signature(properties: Dict[str, Dict[str, str]]) -> str:
            # TODO: enum type support, fix approximations
            return "\n".join(
                [
                    f"{property_name}:{fields['type']},"
                    for property_name, fields in properties.items()
                ]
            )

        return "\n".join(
            [
                f"// {self.description}",
                f"type {self.name} = (_ :{{",
                param_signature(self.properties),
                "}) => any;",
            ]
        )


class OpenAIChatCompletionProvider(LLMChatCompletionProvider):
    """A class to provide chat messages from the OpenAI API."""

    def __init__(
        self,
        model: str = "gpt-4",
        temperature: float = 0.7,
        stream: bool = False,
        functions: List[OpenAIFunction] = [],
        conversation: OpenAIConversation = OpenAIConversation(),
    ) -> None:
        self.model = model
        self.temperature = temperature
        self.stream = stream
        self.functions = functions
        self.conversation = conversation
        set_openai_api_key()

    @property
    def approximate_tokens_consumed(self) -> int:
        """
        A method for approximating the total tokens consumed by the chat instance.

        Note:
            This method can be made handling chat messages and functions identically to OpenAI.
        """
        encoding = tiktoken.encoding_for_model(self.model)
        result = ""
        for ele in self.conversation.get_messages_for_next_completion():
            result += f"{ele['role']}:\n{ele['content']}\n\n"

        result += "\n".join(ele.prompt_format for ele in self.functions)
        return len(encoding.encode(result))

    def get_next_assistant_completion(self) -> OpenAIChatMessage:
        functions = [ele.to_dict() for ele in self.functions]
        logger.debug(
            f"Approximately {self.approximate_tokens_consumed} tokens were consumed prior to completion generation."
        )
        if functions:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=self.conversation.get_messages_for_next_completion(),
                functions=functions,
                function_call="auto",  # auto is default, but we'll be explicit
                stream=self.stream,
            )
        else:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=self.conversation.get_messages_for_next_completion(),
                stream=self.stream,
            )
        if self.stream:
            response = OpenAIChatCompletionProvider._stream_message(
                response_summary=response
            )
            return response

        return OpenAIChatMessage.from_completion_result(
            OpenAIChatCompletionResult(raw_data=response)
        )

    def reset(self) -> None:
        self.conversation.reset_conversation()

    def standalone_call(self, prompt: str) -> str:
        """Return the completion message based on the provided prompt."""
        if self.conversation.messages:
            raise ValueError(
                "The conversation is not empty. Please call reset() before calling standalone_call()."
            )
        self.add_message(LLMChatMessage(role="user", content=prompt))
        response = self.get_next_assistant_completion().content
        self.reset()
        if not response:
            raise ValueError("No response found")
        return response

    def add_message(self, message: LLMChatMessage) -> None:
        if not isinstance(message, OpenAIChatMessage):
            self.conversation.add_message(
                OpenAIChatMessage(role=message.role, content=message.content)
            )
        else:
            self.conversation.add_message(message)
        logger.debug(
            f"Approximately {self.approximate_tokens_consumed} tokens were after adding the latest message."
        )

    @staticmethod
    def _stream_message(response_summary: Any) -> OpenAIChatMessage:
        """Streams the response message from the agent."""
        response = {
            "role": "assistant",
            "content": None,
            "function_call": {
                "name": None,
                "arguments": "",
            },
        }
        latest_accumulation = ""
        stream_separator = " "

        def process_delta(delta, response):
            nonlocal latest_accumulation
            if "content" in delta:
                delta_content = delta["content"]
                if delta_content:
                    if response["content"] is None:
                        response["content"] = delta_content
                    else:
                        response["content"] += delta_content
                    latest_accumulation += delta_content

            if "function_call" in delta:
                delta_function_call = delta["function_call"]
                if delta_function_call:
                    if "name" in delta_function_call:
                        response["function_call"][
                            "name"
                        ] = delta_function_call["name"]
                        latest_accumulation += f'Function Call:\n{delta_function_call["name"]}\n\nArguments:\n'

                    if "arguments" in delta_function_call:
                        response["function_call"][
                            "arguments"
                        ] += delta_function_call["arguments"]
                        latest_accumulation += delta_function_call["arguments"]

            if stream_separator in latest_accumulation:
                words = latest_accumulation.split(stream_separator)
                for word in words[:-1]:
                    print(colored(str(word), "green"), end=" ", flush=True)
                latest_accumulation = words[-1]

        for chunk in response_summary:
            delta = chunk["choices"][0]["delta"]
            process_delta(delta, response)

        if latest_accumulation != "":
            print(
                colored(f"{latest_accumulation}\n\n", "green"),
                end=" ",
                flush=True,
            )
        else:
            print(colored("\n\n", "green"), end=" ", flush=True)

        role = response["role"]
        if not isinstance(role, str):
            raise ValueError("Expected role to be a string")

        function_call = response["function_call"]
        if not isinstance(function_call, dict):
            raise ValueError("Expected function_call to be a dict")

        content = response["content"]
        if content and not isinstance(content, str):
            raise ValueError("Expected content to be a string")

        return OpenAIChatMessage(
            role=role,
            content=content,  # type: ignore
            function_call=FunctionCall.from_response_dict(function_call)  # type: ignore
            if function_call["name"] is not None
            else None,
        )


class OpenAIEmbeddingProvider(EmbeddingVectorProvider):
    """A class to provide embeddings from the OpenAI API."""

    def __init__(self, engine: str = "text-embedding-ada-002") -> None:
        self.engine = engine
        set_openai_api_key()

    def build_embedding_vector(self, source: str) -> np.ndarray:
        """Gets an embedding for the given source text."""
        # wait to import build_embedding_vector to allow easy mocking of the function in tests.
        from openai.embeddings_utils import get_embedding

        return np.array(get_embedding(source, engine=self.engine))

    def batch_build_embedding_vector(
        self, sources: List[str]
    ) -> List[np.ndarray]:
        from openai.embeddings_utils import get_embeddings

        return [
            np.array(ele)
            for ele in get_embeddings(sources, engine=self.engine)
        ]


class OpenAITool(Tool):
    """A class representing a tool that can be used by the OpenAI agent."""

    properties: Dict[str, Dict[str, str]]
    required: List[str]
    openai_function: OpenAIFunction

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
        super().__init__(
            function=function,
            name=name,
            description=description,
            properties=properties,  # type: ignore
            required=required or [],  # type: ignore
            openai_function=OpenAIFunction(  # type: ignore
                name=name,
                description=description,
                properties=properties,
                required=required or [],
            ),
            **kwargs,
        )
