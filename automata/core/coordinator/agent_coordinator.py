from typing import Dict, List, Optional, Type

from pydantic import BaseModel

from automata.configs.automata_agent_configs import AutomataAgentConfig
from automata.core.agent.automata_agent import MasterAutomataAgent
from automata.core.agent.automata_agent_builder import AutomataAgentBuilder
from automata.core.agent.automata_actions import AgentAction
from automata.core.base.tool import Toolkit, ToolkitType


class AgentInstance(BaseModel):
    name: str = ""
    description: str = ""
    config: AutomataAgentConfig = AutomataAgentConfig()
    builder: Type[AutomataAgentBuilder] = AutomataAgentBuilder
    llm_toolkits: Optional[Dict[ToolkitType, Toolkit]] = None

    def run(self, instructions: str) -> str:
        """Runs the agent with the given instructions."""
        agent_builder = self.builder(config=self.config)
        if self.llm_toolkits:
            agent_builder = agent_builder.with_llm_toolkits(self.llm_toolkits)

        agent = agent_builder.with_instructions(instructions).build()
        result = agent.run()
        del agent
        return result

    class Config:
        arbitrary_types_allowed = True


class AgentCoordinator:
    def __init__(self):
        self.agent_instances: List[AgentInstance] = []

    def add_agent_instance(self, agent_instance):
        """Adds an agent instance."""
        # Check agent has not already been added via name field
        if agent_instance.name in [ele.name for ele in self.agent_instances]:
            raise ValueError("Agent already exists.")
        self.agent_instances.append(agent_instance)

    def remove_agent_instance(self, agent_name):
        """Removes an agent instance by name."""
        # Check agent has already been added via name field
        if agent_name not in [ele.name for ele in self.agent_instances]:
            raise ValueError("Agent does not exist.")
        self.agent_instances = [
            instance for instance in self.agent_instances if instance.name != agent_name
        ]

    def set_master_agent(self, master_agent: MasterAutomataAgent):
        """Sets the master agent."""
        self.master_agent = master_agent

    def run_agent(self, action: AgentAction) -> str:
        """Runs the selected agent and returns the result."""
        # Run the selected agent and return the result
        try:
            agent_instance = self._select_agent_instance(action.agent_name)
            output = agent_instance.run("\n".join(action.agent_instruction))
            return output
        except Exception as e:
            return str("Execution fail with error: " + str(e))

    def build_agent_message(self) -> str:
        """Builds a message containing all agents and their descriptions."""
        return "".join(
            [f"\n{agent.name}: {agent.description}\n" for agent in self.agent_instances]
        )

    def _select_agent_instance(self, agent_name) -> AgentInstance:
        """Selects an agent instance by name."""
        for agent in self.agent_instances:
            if agent.name == agent_name:
                return agent
        raise ValueError("Agent does not exist.")
