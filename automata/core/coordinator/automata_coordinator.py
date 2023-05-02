from typing import List

from automata.configs.config_enums import AgentConfigVersion
from automata.core.agent.automata_actions import AgentAction
from automata.core.agent.automata_agent import MasterAutomataAgent
from automata.core.coordinator.automata_instance import AutomataInstance


class AutomataCoordinator:
    def __init__(self):
        """Initializes the coordinator."""
        self.agent_instances: List[AutomataInstance] = []

    def add_agent_instance(self, agent_instance: AutomataInstance) -> None:
        """Adds an agent instance."""
        # Check agent has not already been added via name field
        if agent_instance.config_version in [ele.config_version for ele in self.agent_instances]:
            raise ValueError("Agent already exists.")
        self.agent_instances.append(agent_instance)

    def remove_agent_instance(self, config_version: AgentConfigVersion) -> None:
        """Removes an agent instance by name."""
        # Check agent has already been added via name field
        if config_version not in [ele.config_version for ele in self.agent_instances]:
            raise ValueError("Agent does not exist.")
        self.agent_instances = [
            instance
            for instance in self.agent_instances
            if instance.config_version != config_version
        ]

    def set_master_agent(self, master_agent: MasterAutomataAgent):
        """Sets the master agent."""
        self.master_agent = master_agent

    def run_agent(self, action: AgentAction) -> str:
        """Runs the selected agent and returns the result."""
        # Run the selected agent and return the result
        try:
            agent_instance = self._select_agent_instance(action.agent_version)
            output = agent_instance.run("\n".join(action.agent_instruction))
            return output
        except Exception as e:
            return str("Execution fail with error: " + str(e))

    def build_agent_message(self) -> str:
        """Builds a message containing all agents and their descriptions."""
        return "".join(
            [
                f"\n{agent.config_version.value}: {agent.description}\n"
                for agent in self.agent_instances
            ]
        )

    def _select_agent_instance(self, config_version: AgentConfigVersion) -> AutomataInstance:
        """Selects an agent instance by name."""
        for agent in self.agent_instances:
            if agent.config_version == config_version:
                return agent
        raise ValueError("Agent does not exist.")
