# AutomataCoordinator and AutomataInstance Documentation

## Overview

The AutomataCoordinator is responsible for managing multiple AutomataAgents, including the MasterAutomataAgent. It allows them to work together to perform various tasks and generate results. The AutomataInstance is a representation of an AutomataAgent, including its configuration, description, and builder class.

In this documentation, you will learn how to create and use an AutomataCoordinator and AutomataInstance, as well as how to run multiple AutomataAgents and handle their actions and results.

## Usage

To use the AutomataCoordinator, first create an instance of it. Then, you can create and add multiple AutomataInstances with different configurations and builders. After setting the master agent for the AutomataCoordinator, you can run the agents and retrieve their results.

To create an AutomataInstance, you need to provide its configuration version, description, and builder class. You can then add the AutomataInstance to the AutomataCoordinator.

## Examples

### Creating an AutomataCoordinator and AutomataInstance

```python
from core.coordinator.automata_coordinator import AutomataCoordinator
from core.coordinator.automata_instance import AutomataInstance
from core.agent.automata_agent_builder import AutomataAgentBuilder
from automata.configs.config_enums import AgentConfigVersion

# Create an AutomataCoordinator
coordinator = AutomataCoordinator()

# Create an AutomataInstance
agent_instance = AutomataInstance(
    config_version=AgentConfigVersion.TEST,
    description="Agent 1",
    builder=AutomataAgentBuilder
)

# Add the AutomataInstance to the coordinator
coordinator.add_agent_instance(agent_instance)
```

### Running Multiple Agents

Refer to the "Advanced Implementation Examples" section in the AutomataAgent documentation for a comprehensive example of creating an AutomataCoordinator, adding multiple AutomataInstances, and running the agents to perform different tasks.

## References

### AutomataCoordinator

- `add_agent_instance(instance: AutomataInstance)`: Add an AutomataInstance to the AutomataCoordinator.
- `set_master_agent(agent: MasterAutomataAgent)`: Set the master agent for the AutomataCoordinator.
- `run_agent(action: AgentAction)`: Run an agent based on the given AgentAction instance and return the results.
- `build_agent_message()`: Build a message containing a list of agent instances and descriptions.

### AutomataInstance

- `__init__(self, config_version: AgentConfigVersion, description: str, builder: Type[AutomataAgentBuilder])`: Initialize an AutomataInstance with the provided configuration version, description, and builder class.

### Eval

Refer to the provided "Eval Class" code and docstring for a detailed description of the Eval class, its methods, and usage in evaluating an agent's performance when given a set of instructions.

## Additional Resources

For more information on the AutomataAgent, MasterAutomataAgent, and associated classes, refer to the AutomataAgent documentation provided.
