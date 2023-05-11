from automata.core.agent.automata_agent import AutomataAgent
from automata.core.coordinator.automata_coordinator import AutomataCoordinator


class AutomataManager:
    def __init__(
        self,
        main_agent: AutomataAgent,
        coordinator: AutomataCoordinator,
    ):
        self.main_agent = main_agent
        self.coordinator = coordinator

    def run(self):
        # system execution logic
        self.main_agent.run()

    def replay_messages(self):
        # system execution logic
        self.main_agent.replay_messages()
