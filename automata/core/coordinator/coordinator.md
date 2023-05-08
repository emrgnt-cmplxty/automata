# AutomataCoordinator Documentation

## Overview

The AutomataCoordinator is responsible for managing multiple AutomataInstances. It provides methods for adding and removing agent instances, setting a master agent, executing actions on agent instances, and building agent messages.

The AutomataInstance represents an individual agent instance with a specific configuration. It provides a method to execute instructions on the agent.

## Usage

### AutomataCoordinator

1. Initialize an AutomataCoordinator:

   ```python
   coordinator = AutomataCoordinator()
   ```

2. Add an AutomataInstance to the coordinator:

   ```python
   coordinator.add_agent_instance(agent_instance)
   ```

3. Remove an AutomataInstance from the coordinator by its config_version:

   ```python
   coordinator.remove_agent_instance(config_version)
   ```

4. Set the master agent for the AutomataCoordinator:

   ```python
   coordinator.set_master_agent(master_agent)
   ```

5. Execute an action on the selected agent instance:

   ```python
   coordinator.run_agent(action)
   ```

6. Build a message containing the configuration version and description of all managed agent instances:

   ```python
   coordinator.build_agent_message()
   ```

### AutomataInstance

1. Execute instructions on the agent:

   ```python
   instance.run(instructions)
   ```

## Examples

### AutomataCoordinator

```python
from automata.configs.config_enums import AgentConfigVersion
from automata.core.agent.automata_actions import AgentAction
from automata.core.agent.automata_agent import MasterAutomataAgent
from automata.core.coordinator.automata_instance import AutomataInstance
from automata.core.coordinator.automata_coordinator import AutomataCoordinator

# Initialize coordinator
coordinator = AutomataCoordinator()

# Create an agent instance with a specific configuration
instance = AutomataInstance(config_version=AgentConfigVersion.V1)

# Add the agent instance to the coordinator
coordinator.add_agent_instance(instance)

# Remove the agent instance from the coordinator
coordinator.remove_agent_instance(AgentConfigVersion.V1)

# Execute an action on the agent instance
action = AgentAction("some_action")
result = coordinator.run_agent(action)
print(result)

# Build a message containing information about managed agent instances
message = coordinator.build_agent_message()
print(message)
```

### AutomataInstance

```python
from automata.core.coordinator.automata_instance import AutomataInstance
from automata.configs.config_enums import AgentConfigVersion

# Create an agent instance with a specific configuration
instance = AutomataInstance(config_version = AgentConfigVersion.V1)

# Execute instructions on the agent instance
instructions = "some_instruction"
result = instance.run(instructions)
print(result)
```

## References

- core.coordinator.automata_instance
  - AutomataInstance
    - run
    - Config
- core.coordinator.automata_coordinator
  - AutomataCoordinator
    - add_agent_instance
    - remove_agent_instance
    - set_master_agent
    - run_agent
    - build_agent_message
- cli.scripts.run_coordinator
  - configure_logging
  - create_coordinator
  - create_master_agent
  - check_input
  - run
  - main
- core.coordinator.automata_coordinator.**init**
- core.coordinator.automata_coordinator.AutomataCoordinator
- core.coordinator.automata_coordinator.add_agent_instance
- core.coordinator.automata_coordinator.remove_agent_instance
