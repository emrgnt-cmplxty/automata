from typing import TYPE_CHECKING, Any, Dict

from pydantic import BaseModel

from automata.config.base import AgentConfigName
from automata.config.openai_agent import AutomataOpenAIAgentConfigBuilder
from automata.core.agent.agent import AgentInstance

if TYPE_CHECKING:
    from automata.core.agent.providers import OpenAIAutomataAgent


class OpenAIAutomataAgentInstance(AgentInstance, BaseModel):
    """
    An instance of an Automata OpenAI agent.

    This class stores the instructions and configuration for an agent
    So that it can be run multiple times without having to reinitialize
    the agent each time.
    """

    config_name: AgentConfigName = AgentConfigName.DEFAULT
    description: str = ""
    kwargs: Dict[str, Any] = {}

    class Config:
        arbitrary_types_allowed = True

    def run(self, instructions: str) -> str:
        """
        Executes the specified instructions on an agent built
        from this instance's configuration and returns the result.

        Raises:
            Exception: If any error occurs during agent execution.
        """
        config = AutomataOpenAIAgentConfigBuilder.create_from_args(
            config_to_load=self.config_name, **self.kwargs
        )

        agent = OpenAIAutomataAgent(instructions, config=config)
        result = agent.run()
        del agent
        return result
