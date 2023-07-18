import json
from typing import Any, Dict, List

from automata.config import AgentConfig, OpenAIAutomataAgentConfig
from automata.llm.foundation import LLMChatMessage
from automata.llm.providers import OpenAIChatMessage

from .base import Action, Eval


class OpenAIFunctionCallAction(Action):
    """An action represented by a function call."""

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
    """A class for evaluating an OpenAI LLM."""

    def __init__(self, config: AgentConfig, *args, **kwargs):
        assert isinstance(config, OpenAIAutomataAgentConfig)
        super().__init__(config, *args, **kwargs)

    def _extract_action(self, message: LLMChatMessage) -> List[Action]:
        actions: List[Action] = []
        if isinstance(message, OpenAIChatMessage):
            function_call = message.function_call
            if function_call:
                action = OpenAIFunctionCallAction(
                    name=function_call.name, arguments=function_call.arguments
                )
                actions.append(action)
        return actions
