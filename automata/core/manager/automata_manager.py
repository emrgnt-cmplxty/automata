from automata.core.agent.automata_agent import AutomataAgent
from automata.core.coordinator.automata_coordinator import AutomataCoordinator


class AutomataManager:
    """
    Class for managing the execution of the Automata system.
    """

    def __init__(
        self,
        main_agent: AutomataAgent,
        coordinator: AutomataCoordinator,
    ):
        """
        Initializes the AutomataManager.
        :param main_agent: The main agent to be run.
        :param coordinator: The coordinator to be run.
        """
        self.main_agent = main_agent
        self.coordinator = coordinator

    def run(self) -> str:
        # system execution logic
        return self.main_agent.run()
