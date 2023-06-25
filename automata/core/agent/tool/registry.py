from abc import ABC, abstractmethod
from typing import List, Any, Type
from automata.core.base.agent import AgentToolBuilder
from automata.core.llm.providers.openai import OpenAIAgentToolBuilder, OpenAITool


class AutomataOpenAIAgentToolBuilderRegistry:
    _all_builders: List[Type[OpenAIAgentToolBuilder]] = []

    @staticmethod
    def register_tool_manager(cls: Type[OpenAIAgentToolBuilder]):
        AutomataOpenAIAgentToolBuilderRegistry._all_builders.append(cls)
        return cls

    @staticmethod
    def get_all_builders() -> List[Type[OpenAIAgentToolBuilder]]:
        return AutomataOpenAIAgentToolBuilderRegistry._all_builders
