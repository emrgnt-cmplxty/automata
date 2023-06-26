from abc import ABC, abstractmethod
from typing import Any, List, Set, Type

from automata.core.base.agent import AgentToolBuilder
from automata.core.llm.providers.openai import OpenAIAgentToolBuilder, OpenAITool


class AutomataOpenAIAgentToolBuilderRegistry:
    _all_builders: Set[Type[OpenAIAgentToolBuilder]] = set([])

    @staticmethod
    def register_tool_manager(cls: Type[OpenAIAgentToolBuilder]):
        AutomataOpenAIAgentToolBuilderRegistry._all_builders.add(cls)
        return cls

    @staticmethod
    def get_all_builders() -> List[Type[OpenAIAgentToolBuilder]]:
        # FIXME - This is a hack to ensure that all builders are registered
        # We should find a better way to do this
        # Import builders so that we can be sure they are registered with the registry
        from automata.core.agent.tool.builder.context_oracle import (  # type : ignore
            ContextOracleOpenAIToolBuilder,
        )
        from automata.core.agent.tool.builder.py_reader import (  # type : ignore
            PyReaderOpenAIToolBuilder,
        )
        from automata.core.agent.tool.builder.py_writer import (  # type : ignore
            PyWriterOpenAIToolBuilder,
        )
        from automata.core.agent.tool.builder.symbol_search import (  # type : ignore
            SymbolSearchOpenAIToolBuilder,
        )

        return list(AutomataOpenAIAgentToolBuilderRegistry._all_builders)
