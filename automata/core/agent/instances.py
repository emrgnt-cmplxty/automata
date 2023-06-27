from typing import TYPE_CHECKING, Any, Dict

from pydantic import BaseModel

from automata.config.base import AgentConfigName
from automata.config.openai_agent import AutomataOpenAIAgentConfigBuilder
from automata.core.base.agent import AgentInstance

if TYPE_CHECKING:
    from automata.core.agent.agents import AutomataOpenAIAgent


class AutomataOpenAIAgentInstance(AgentInstance, BaseModel):
    """An instance of an Automata OpenAI agent."""

    config_name: AgentConfigName = AgentConfigName.DEFAULT
    description: str = ""
    kwargs: Dict[str, Any] = {}

    def run(self, instructions: str) -> str:
        """
        Executes the specified instructions on an agent built from this instance's configuration
        and returns the result.

        Args:
            instructions (str): The instructions to be executed by the agent.

        Returns:
            str: The output produced by the agent.

        Raises:
            Exception: If any error occurs during agent execution.
        """
        config = AutomataOpenAIAgentConfigBuilder.create_from_args(
            config_to_load=self.config_name, **self.kwargs
        )

        agent = AutomataOpenAIAgent(instructions, config=config)
        result = agent.run()
        del agent
        return result

    class Config:
        arbitrary_types_allowed = True
