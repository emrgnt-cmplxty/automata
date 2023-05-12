from typing import Any, Dict

from pydantic import BaseModel

from automata.configs.automata_agent_config_utils import AutomataAgentConfigFactory
from automata.configs.config_enums import AgentConfigName
from automata.core.agent.automata_agent_utils import AutomataAgentFactory


class AutomataInstance(BaseModel):
    config_name: AgentConfigName = AgentConfigName.DEFAULT
    description: str = ""
    kwargs: Dict[str, Any] = {}

    @classmethod
    def create(cls, config_name: AgentConfigName, description: str = "", **kwargs):
        return cls(config_name=config_name, description=description, kwargs=kwargs)

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
        main_config = AutomataAgentConfigFactory.create_config(**self.kwargs)

        agent = AutomataAgentFactory.create_agent(instructions, config=main_config)
        result = agent.run()
        del agent
        return result

    class Config:
        arbitrary_types_allowed = True
