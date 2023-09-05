"""
A central coordinating agent that spawns and terminates agents based on their performance.
"""

from automata.agent.openai_agent import OpenAIAutomataAgent
from automata.config import OpenAIAutomataAgentConfig

class CentralAgent:
    def __init__(self, max_agents=5):
        self.max_agents = max_agents
        self.active_agents = []

    def run(self):
        # Initialize agents
        config_for_agent = OpenAIAutomataAgentConfig(
            model="some_model",
            temperature=0.8,
            stream=True,
            system_instruction="Your system instruction here",
            max_iterations=20,
        )

        for _ in range(self.max_agents):
            agent = OpenAIAutomataAgent("TODO: prompt", config_for_agent)
            self.active_agents.append(agent)

        while self.should_continue():
            results = [agent.run() for agent in self.active_agents]
            
            # Use results to decide which agents to keep, terminate, or spawn
            self.evaluate_and_manage_agents(results)

    def should_continue(self):
        #TODO: implement
        # Implement stopping criterion, e.g., max iterations or satisfactory solution found
        # Make this a tool?
        pass

    def evaluate_and_manage_agents(self, results):
        #TODO: implement
        # Evaluate agent results
        # Terminate poorly performing agents
        # Spawn new agents if necessary
        pass