import logging
from typing import Dict

from automata.configs.automata_agent_configs import AgentConfigName, AutomataAgentConfig
from automata.core.agent.automata_agent import AutomataAgent
from automata.core.coordinator.automata_coordinator_utils import AutomataCoordinatorFactory
from automata.core.manager.automata_manager import AutomataManager

logger = logging.getLogger(__name__)


class AutomataManagerFactory:
    """
    Class for creating AutomataManager instances.
    """

    @staticmethod
    def create_manager(
        main_agent: AutomataAgent,
        helper_agent_configs: Dict[AgentConfigName, AutomataAgentConfig],
    ) -> AutomataManager:
        """
        Create AutomataManager instance from a coordinator and a main agent.
        :param main_agent: AutomataAgent instance.
        :param helper_agent_configs: Dictionary of AutomataAgentConfig instances, keyed on AgentConfigName.
        :return: AutomataManager instance.
        """
        logging.info(
            f"Creating AutomataCoordinator from helper_agent_configs={helper_agent_configs}"
        )
        coordinator = AutomataCoordinatorFactory.create_coordinator(
            main_agent, helper_agent_configs
        )
        logging.info(
            f"Creating AutomataManager with main_agent={main_agent} and coordinator={coordinator}"
        )
        return AutomataManager(main_agent, coordinator)
