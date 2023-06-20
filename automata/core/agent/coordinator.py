from typing import TYPE_CHECKING, Any, Dict, List

from pydantic import BaseModel

from automata.config.agent_config_builder import AutomataAgentConfigFactory
from automata.config.config_types import AgentConfigName
from automata.core.agent.action import AgentAction

if TYPE_CHECKING:
    from automata.core.agent.agent import AutomataAgent


class AutomataInstance(BaseModel):
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

        agent = AutomataAgent(instructions, config=main_config)
        agent.setup()
        result = agent.run()
        del agent
        return result

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def create(
        cls, config_name: AgentConfigName, description: str = "", **kwargs
    ) -> "AutomataInstance":
        return cls(config_name=config_name, description=description, kwargs=kwargs)


class AutomataCoordinator:
    def __init__(self) -> None:
        """
        Initializes the AutomataCoordinator, which is responsible for managing
        multiple AutomataInstances.
        """
        self.agent_instances: List[AutomataInstance] = []

    def add_agent_instance(self, agent_instance: AutomataInstance) -> None:
        """
        Adds a new AutomataInstance to the list of managed agent instances.

        Args:
            agent_instance (AutomataInstance): The agent instance to be added.

        Raises:
            ValueError: If an agent with the same config_name already exists in the list.
        """
        # Check agent has not already been added via name field
        if agent_instance.config_name in [ele.config_name for ele in self.agent_instances]:
            raise ValueError("Agent already exists.")
        self.agent_instances.append(agent_instance)

    def remove_agent_instance(self, config_name: AgentConfigName) -> None:
        """
        Removes an AutomataInstance from the list of managed agent instances by its config_name.

        Args:
            config_name (AgentConfigName): The configuration version of the agent instance to be removed.

        Raises:
            ValueError: If the specified agent instance does not exist in the list.
        """
        # Check agent has already been added via name field
        if config_name not in [ele.config_name for ele in self.agent_instances]:
            raise ValueError("Agent does not exist.")
        self.agent_instances = [
            instance for instance in self.agent_instances if instance.config_name != config_name
        ]

    def set_main_agent(self, main_agent: "AutomataAgent") -> None:
        """
        Sets the main agent for the AutomataCoordinator.

        Args:
            main_agent (AutomataAgent): The main agent to be set.
        """
        self.main_agent = main_agent

    def run_agent(self, action: AgentAction) -> str:
        """
        Executes the specified action on the selected agent instance and returns the result.

        Args:
            action (AgentAction): The action to be executed on the agent instance.

        Returns:
            str: The output produced by the agent instance.

        Raises:
            ValueError: If the specified agent instance does not exist.
        """
        # Run the selected agent and return the result
        try:
            agent_instance = self._select_agent_instance(action.agent_version)
            output = agent_instance.run("\n".join(action.agent_instruction))
            return output
        except Exception as e:
            return str("Execution fail with error: " + str(e))

    def _select_agent_instance(self, config_name: AgentConfigName) -> AutomataInstance:
        """
        Retrieves an AutomataInstance from the list of managed agent instances by its config_name.

        Args:
            config_name (AgentConfigName): The configuration version of the desired agent instance.

        Returns:
            AutomataInstance: The selected agent instance.

        Raises:
            ValueError: If the specified agent instance does not exist.
        """
        for agent in self.agent_instances:
            if agent.config_name == config_name:
                return agent
        raise ValueError("Agent does not exist.")
