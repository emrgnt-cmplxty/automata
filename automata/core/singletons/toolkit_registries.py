import pkgutil
from typing import List, Set, Type

from automata.core.base.patterns.singleton import Singleton
from automata.core.agent.providers import OpenAIAgentToolkitBuilder


class OpenAIAutomataAgentToolkitRegistry(metaclass=Singleton):
    _all_builders: Set[Type[OpenAIAgentToolkitBuilder]] = set([])
    _is_initialized: bool = False

    @staticmethod
    def register_tool_manager(cls: Type[OpenAIAgentToolkitBuilder]):
        OpenAIAutomataAgentToolkitRegistry._all_builders.add(cls)
        return cls

    @staticmethod
    def get_all_builders() -> List[Type[OpenAIAgentToolkitBuilder]]:
        """
        Get all the registered tool builders.
        Initializes the builder registry if it has not been initialized yet.
        """
        # Ensure that the registry is initialized
        if not OpenAIAutomataAgentToolkitRegistry._is_initialized:
            OpenAIAutomataAgentToolkitRegistry.initialize()
        return list(OpenAIAutomataAgentToolkitRegistry._all_builders)

    @staticmethod
    def initialize():
        """
        Initializes the registry builders by calling an import on the modules in the builder package.
        This triggers the registration of the builders through the register_tool_manager decorator.
        """
        # Check if the registry has already been initialized
        if OpenAIAutomataAgentToolkitRegistry._is_initialized:
            return
        # Import all builder modules to ensure the classes get registered
        import automata.core.tools.builders as builder_package

        for _, module_name, _ in pkgutil.iter_modules(builder_package.__path__):
            __import__(f"automata.core.tools.builders.{module_name}", fromlist=[""])

        # Mark the registry as initialized
        OpenAIAutomataAgentToolkitRegistry._is_initialized = True


open_ai_agent_toolkit_registry = OpenAIAutomataAgentToolkitRegistry()
