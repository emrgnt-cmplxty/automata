from abc import abstractmethod
from typing import TYPE_CHECKING, Any, Dict

from pydantic import BaseModel

from automata.config.agent_config_builder import AutomataAgentConfigFactory
from automata.config.config_types import AgentConfigName

if TYPE_CHECKING:
    from automata.core.agent.agent import AutomataOpenAIAgent


class AgentInstance(BaseModel):
    config_name: AgentConfigName = AgentConfigName.DEFAULT
    description: str = ""
    kwargs: Dict[str, Any] = {}

    class Config:
        arbitrary_types_allowed = True

    @abstractmethod
    def run(self, instructions: str) -> str:
        pass

    @classmethod
    def create(
        cls, config_name: AgentConfigName, description: str = "", **kwargs
    ) -> "AgentInstance":
        return cls(config_name=config_name, description=description, kwargs=kwargs)


class AutomataOpenAIAgentInstance(AgentInstance, BaseModel):
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
        main_config = AutomataAgentConfigFactory.create_config(
            main_config_name=self.config_name, **self.kwargs
        )

        agent = AutomataOpenAIAgent(instructions, config=main_config)
        result = agent.run()
        del agent
        return result

    class Config:
        arbitrary_types_allowed = True
