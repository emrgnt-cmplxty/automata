import json
from typing import Any, Dict, List

from automata.agent import Agent, AgentProvider
from automata.config import AgentConfig, OpenAIAutomataAgentConfig
from .code_writing import CodeWritingEval
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


class OpenAIEval(Eval):
    "An abstract class for evaluating an OpenAI LLM."

    def _build_and_run_agent(self, instructions: str) -> Agent:
        from automata.agent.providers import (  # import late for mocking in tests
            OpenAIAutomataAgent,
        )

        if not isinstance(self.config, OpenAIAutomataAgentConfig):
            raise TypeError(
                "Expected OpenAIAutomataAgentConfig, found: {self.config.__class__.__name__}"
            )

        agent = OpenAIAutomataAgent(
            instructions=instructions, config=self.config
        )
        agent.run()
        return agent


class OpenAIFunctionEval(OpenAIEval):
    """A concrete class for evaluating an OpenAI messages for function call actions."""

    def __init__(self, config: AgentConfig, *args, **kwargs):
        assert isinstance(config, OpenAIAutomataAgentConfig)
        super().__init__(config, *args, **kwargs)

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
