"""
This file defines the classes for how to manage prompts for different types of
models, i.e., "chat models" vs. "non chat models".
"""
import logging
import threading
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, NamedTuple, Union

logger = logging.getLogger(__name__)
ENCODER_LOCK = threading.Lock()

# This is an approximation to the type accepted as the `prompt` field to `openai.Completion.create` calls
OpenAICreatePrompt = Union[str, List[str], List[int], List[List[int]]]


# This is the type accepted as the `prompt` field to `openai.ChatCompletion.create` calls
class OpenAIChatMessage(NamedTuple):
    role: str
    content: str

    def to_dict(self) -> Dict[str, str]:
        return {"role": self.role, "content": self.content}


OpenAICreateChatPrompt = List[OpenAIChatMessage]  # A chat log is a list of messages


def chat_prompt_to_text_prompt(prompt: OpenAICreateChatPrompt, for_completion: bool = True) -> str:
    """
    Render a chat prompt as a text prompt. User and assistant messages are separated by newlines
    and prefixed with "User: " and "Assistant: ", respectively, unless there is only one message.
    System messages have no prefix.
    """
    assert is_chat_prompt(prompt), f"Expected a chat prompt, got {prompt}"
    chat_to_prefixes = {
        # roles
        "system": "",
        # names
        "example_user": "User: ",
        "example_assistant": "Assistant: ",
    }

    # For a single message, be it system, user, or assistant, just return the message
    if len(prompt) == 1:
        return prompt[0].content

    text = ""
    for msg in prompt:
        role = msg.role
        prefix = chat_to_prefixes.get(role, role.capitalize() + ": ")
        content = msg.content
        text += f"{prefix}{content}\n"
    if for_completion:
        text += "Assistant: "
    return text.lstrip()


def text_prompt_to_chat_prompt(prompt: str, role: str = "system") -> OpenAICreateChatPrompt:
    assert isinstance(prompt, str), f"Expected a text prompt, got {prompt}"
    return [
        OpenAIChatMessage(role=role, content=prompt),
    ]


@dataclass
class Prompt(ABC):
    """
    A `Prompt` encapsulates everything required to present the `raw_prompt` in different formats,
    e.g., a normal unadorned format vs. a chat format.
    """

    @abstractmethod
    def to_formatted_prompt(self):
        """
        Return the actual data to be passed as the `prompt` field to your model.
        See the above types to see what each API call is able to handle.
        """


# TODO - Change input type
def is_chat_prompt(prompt: Any) -> bool:
    return isinstance(prompt, list) and all(isinstance(msg, dict) for msg in prompt)


@dataclass
class CompletionPrompt(Prompt):
    """
    A `Prompt` object that wraps prompts to be compatible with non chat models, which use `openai.Completion.create`.
    """

    raw_prompt: Union[str, OpenAICreateChatPrompt]

    # TODO - Why is the prompt failing?
    def _render_chat_prompt_as_text(self, prompt: Any) -> str:
        return chat_prompt_to_text_prompt(prompt)

    def to_formatted_prompt(self) -> str:
        if is_chat_prompt(self.raw_prompt):
            return self._render_chat_prompt_as_text(self.raw_prompt)
        return self.raw_prompt  # type: ignore


class CompletionResult(ABC):
    @abstractmethod
    def get_completions(self) -> list[str]:
        pass


class OpenAIBaseCompletionResult(CompletionResult):
    def __init__(self, raw_data: Any):
        self.raw_data = raw_data

    def get_completions(self) -> list[str]:
        raise NotImplementedError


class OpenAIChatCompletionResult(OpenAIBaseCompletionResult):
    def get_completion(self) -> str:
        return self.raw_data["choices"][0]["message"]["content"]
