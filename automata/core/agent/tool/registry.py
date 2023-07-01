import pkgutil
from typing import List, Set, Type

from automata.core.agent.providers import OpenAIAgentToolkit


class AutomataOpenAIAgentToolkitRegistry:
    _all_builders: Set[Type[OpenAIAgentToolkit]] = set([])
    _is_initialized: bool = False

    @staticmethod
    def register_tool_manager(cls: Type[OpenAIAgentToolkit]):
        AutomataOpenAIAgentToolkitRegistry._all_builders.add(cls)
        return cls

    @staticmethod
    def get_all_builders() -> List[Type[OpenAIAgentToolkit]]:
        """
        Get all the registered tool builders.
        Initializes the builder registry if it has not been initialized yet.
        """
        # Ensure that the registry is initialized
        if not AutomataOpenAIAgentToolkitRegistry._is_initialized:
            AutomataOpenAIAgentToolkitRegistry.initialize()
        return list(AutomataOpenAIAgentToolkitRegistry._all_builders)

    @staticmethod
    def initialize():
        """
        Initializes the registry builders by calling an import on the modules in the builder package.
        This triggers the registration of the builders through the register_tool_manager decorator.
        """
        # Check if the registry has already been initialized
        if AutomataOpenAIAgentToolkitRegistry._is_initialized:
            return
        # Import all builder modules to ensure the classes get registered
        import automata.core.agent.tool.builder as builder_package

        for _, module_name, _ in pkgutil.iter_modules(builder_package.__path__):
            __import__(f"automata.core.agent.tool.builder.{module_name}", fromlist=[""])

        # Mark the registry as initialized
        AutomataOpenAIAgentToolkitRegistry._is_initialized = True
