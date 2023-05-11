from typing import Any, Dict

from pydantic import BaseModel

from automata.configs.automata_agent_configs import AutomataAgentConfig
from automata.configs.config_enums import AgentConfigVersion
from automata.core.agent.automata_agent_utils import create_builder_from_args


class AutomataInstance(BaseModel):
    config_name: AgentConfigVersion = AgentConfigVersion.DEFAULT
    description: str = ""
    kwargs: Dict[str, Any] = {}

    @classmethod
    def create(cls, config_name: AgentConfigVersion, description: str = "", **kwargs):
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
        self.kwargs["agent_config"] = AutomataAgentConfig.load(self.config_name)

        agent_builder = create_builder_from_args(**self.kwargs)

        agent = agent_builder.with_instructions(instructions).build()
        result = agent.run()
        del agent
        return result

    class Config:
        arbitrary_types_allowed = True
