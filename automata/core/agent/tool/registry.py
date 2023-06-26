import pkgutil
from typing import List, Set, Type

from automata.core.llm.providers.openai import OpenAIAgentToolBuilder


class AutomataOpenAIAgentToolBuilderRegistry:
    _all_builders: Set[Type[OpenAIAgentToolBuilder]] = set([])
    _is_initialized: bool = False

    @staticmethod
    def register_tool_manager(cls: Type[OpenAIAgentToolBuilder]):
        AutomataOpenAIAgentToolBuilderRegistry._all_builders.add(cls)
        return cls

    @staticmethod
    def get_all_builders() -> List[Type[OpenAIAgentToolBuilder]]:
        # Ensure that the registry is initialized
        if not AutomataOpenAIAgentToolBuilderRegistry._is_initialized:
            AutomataOpenAIAgentToolBuilderRegistry.initialize()
        return list(AutomataOpenAIAgentToolBuilderRegistry._all_builders)

    @staticmethod
    def initialize():
        # Check if the registry has already been initialized
        if AutomataOpenAIAgentToolBuilderRegistry._is_initialized:
            return
        # Import all builder modules to ensure the classes get registered
        import automata.core.agent.tool.builder as builder_package

        for _, module_name, _ in pkgutil.iter_modules(builder_package.__path__):
            __import__(f"automata.core.agent.tool.builder.{module_name}", fromlist=[""])

        # Mark the registry as initialized
        AutomataOpenAIAgentToolBuilderRegistry._is_initialized = True
