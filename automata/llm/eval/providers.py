import json
from typing import Any, Dict, List

from automata.agent import AgentProvider, OpenAIAgentProvider
from automata.llm.foundation import LLMChatMessage
from automata.llm.providers import OpenAIChatMessage

from .base import Action, Eval
from .code_writing import CodeWritingEval


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


class OpenAIEval(Eval):
    "An abstract class for evaluating an OpenAI LLM."


class OpenAIFunctionEval(OpenAIEval):
    """A concrete class for evaluating an OpenAI messages for function call actions."""

    def __init__(self, agent_provider: AgentProvider, *args, **kwargs):
        assert isinstance(agent_provider, OpenAIAgentProvider)
        super().__init__(agent_provider, *args, **kwargs)

    def extract_action(self, message: LLMChatMessage) -> List[Action]:
        actions: List[Action] = []
        if isinstance(message, OpenAIChatMessage):
            function_call = message.function_call
            if (
                function_call and function_call.name != "initializer"
            ):  # initialize is a dummy method call
                action = OpenAIFunctionCallAction(
                    name=function_call.name, arguments=function_call.arguments
                )
                actions.append(action)
        return actions


class OpenAICodeWritingEval(OpenAIEval, CodeWritingEval):
    """A concrete class for evaluating an OpenAI LLM's code writing actions."""

    pass
