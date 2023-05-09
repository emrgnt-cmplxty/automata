from typing import List

from automata.configs.config_enums import AgentConfigVersion
from automata.core.agent.automata_actions import AgentAction
from automata.core.agent.automata_agent import MasterAutomataAgent
from automata.core.coordinator.automata_instance import AutomataInstance


class AutomataCoordinator:
    def __init__(self):
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
            ValueError: If an agent with the same config_version already exists in the list.
        """
        # Check agent has not already been added via name field
        if agent_instance.config_version in [ele.config_version for ele in self.agent_instances]:
            raise ValueError("Agent already exists.")
        self.agent_instances.append(agent_instance)

    def remove_agent_instance(self, config_version: AgentConfigVersion) -> None:
        """
        Removes an AutomataInstance from the list of managed agent instances by its config_version.

        Args:
            config_version (AgentConfigVersion): The configuration version of the agent instance to be removed.

        Raises:
            ValueError: If the specified agent instance does not exist in the list.
        """
        # Check agent has already been added via name field
        if config_version not in [ele.config_version for ele in self.agent_instances]:
            raise ValueError("Agent does not exist.")
        self.agent_instances = [
            instance
            for instance in self.agent_instances
            if instance.config_version != config_version
        ]

    def set_master_agent(self, master_agent: MasterAutomataAgent):
        """
        Sets the master agent for the AutomataCoordinator.

        Args:
            master_agent (MasterAutomataAgent): The master agent to be set.
        """
        self.master_agent = master_agent

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

    def build_agent_message(self) -> str:
        """
        Constructs a string message containing the configuration version and description
        of all managed agent instances.

        Returns:
            str: The generated message.
        """
        return "".join(
            [
                f"\n{agent.config_version.value}: {agent.description}\n"
                for agent in self.agent_instances
            ]
        )

    def _select_agent_instance(self, config_version: AgentConfigVersion) -> AutomataInstance:
        """
        Retrieves an AutomataInstance from the list of managed agent instances by its config_version.

        Args:
            config_version (AgentConfigVersion): The configuration version of the desired agent instance.

        Returns:
            AutomataInstance: The selected agent instance.

        Raises:
            ValueError: If the specified agent instance does not exist.
        """
        for agent in self.agent_instances:
            if agent.config_version == config_version:
                return agent
        raise ValueError("Agent does not exist.")
