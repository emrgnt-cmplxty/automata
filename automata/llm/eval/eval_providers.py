import json
from typing import Any, Dict, List

from automata.llm.foundation import LLMChatMessage
from automata.llm.providers import OpenAIChatMessage

from .base import Action, Eval


class OpenAIFunctionCallAction(Action):
    """A concrete action represented by an OpenAI function call."""

    def __init__(self, name: str, arguments: Dict[str, Any]):
        self.name = name
        self.arguments = arguments

    def __eq__(self, other):
        if isinstance(other, OpenAIFunctionCallAction):
            return (
                self.name == other.name and self.arguments == other.arguments
            )
        return False

    def __hash__(self):
        return hash((self.name, json.dumps(self.arguments)))

    def __str__(self):
        return f"{self.name}({self.arguments})"

    def __repr__(self):
        return f"OpenAIFunctionCallAction(name={self.name}, arguments={self.arguments})"
    
    def to_dict(self):
        return {
            "type": "OpenAIFunctionCallAction",
            "name": self.name,
            "arguments": self.arguments
        }

    @staticmethod
    def from_dict(dct):
        return OpenAIFunctionCallAction(
            name=dct["name"],
            arguments=dct["arguments"]
        )


class OpenAIFunctionEval(Eval):
    """A concrete class for evaluating an OpenAI messages for function call actions."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __repr__(self) -> str:
        return "OpenAIFunctionEval()"

    def extract_action(self, message: LLMChatMessage) -> List[Action]:
        """Extracts the coding action explicitly"""

        actions: List[Action] = []
        if isinstance(message, OpenAIChatMessage):
            function_call = message.function_call
            if function_call and function_call.name != "initializer":
                action = OpenAIFunctionCallAction(
                    name=function_call.name, arguments=function_call.arguments
                )
                actions.append(action)
        return actions

    def _filter_actions(self, actions: List[Action]) -> List[Action]:
        """Filters out non-OpenAIFunctionCallActions."""

        return [
            action
            for action in actions
            if isinstance(action, OpenAIFunctionCallAction)
        ]
