import logging
from typing import Dict

from automata.configs.automata_agent_configs import AgentConfigVersion, AutomataAgentConfig
from automata.core.agent.automata_agent import AutomataAgent
from automata.core.coordinator.automata_coordinator import AutomataCoordinator
from automata.core.coordinator.automata_instance import AutomataInstance

logger = logging.getLogger(__name__)


class AutomataCoordinatorFactory:
    @staticmethod
    def create_coordinator(
        main_agent: AutomataAgent,
        helper_agent_configs: Dict[AgentConfigVersion, AutomataAgentConfig],
    ) -> AutomataCoordinator:
        """
        Create AutomataCoordinator and setup agent-main linkage.
        :param main_agent: AutomataAgent instance.
        :param helper_agent_configs: List of AutomataAgentConfig instances.
        :return: AutomataCoordinator instance.
        """
        coordinator = AutomataCoordinator()
        for config_name in helper_agent_configs.keys():
            config = helper_agent_configs[config_name]
            logger.info(
                f"Adding Agent with name={config_name.value}, description={config.description}"
            )
            agent = AutomataInstance(
                config_name=config_name,
                description=config.description,
                verbose=True,
                stream=True,
            )
            coordinator.add_agent_instance(agent)
        main_agent.set_coordinator(coordinator)
        coordinator.set_main_agent(main_agent)
        return coordinator
