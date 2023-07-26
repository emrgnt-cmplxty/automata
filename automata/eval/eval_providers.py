import json
from typing import Dict, List

from automata.eval import Action, AgentEval, Payload
from automata.llm.foundation import LLMChatMessage
from automata.llm.providers import OpenAIChatMessage


class OpenAIFunctionCallAction(Action):
    """A concrete action represented by an OpenAI function call."""

    def __init__(self, name: str, arguments: Dict[str, str]):
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

    def to_payload(self) -> Payload:
        """Converts a OpenAIFunctionCallAction to a valid storage payload object"""

        return {
            "type": "OpenAIFunctionCallAction",
            "name": self.name,
            "arguments": self.arguments,
        }

    @classmethod
    def from_payload(cls, payload: Payload) -> "OpenAIFunctionCallAction":
        """Converts a storage payload into an underlying OpenAIFunctionCallAction object"""

        name = payload["name"]
        if not isinstance(name, str):
            raise ValueError("Payload name was not a string")

        arguments = payload["arguments"]
        if isinstance(arguments, str):
            # TODO - Add special error handling here
            return OpenAIFunctionCallAction(
                name=name, arguments=json.loads(arguments)
            )

        elif not isinstance(arguments, dict):
            raise ValueError("Payload arguments was not a dictionary")

        return OpenAIFunctionCallAction(name=name, arguments=arguments)


class OpenAIFunctionEval(AgentEval):
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
