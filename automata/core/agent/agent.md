# AutomataAgent Documentation

## Overview

The AutomataAgent is an autonomous agent designed to execute instructions and report the results back to the master system. It communicates with the OpenAI API to generate responses based on given instructions and manages interactions with various tools. The MasterAutomataAgent is a specialized AutomataAgent that can interact with an AutomataCoordinator to execute and manipulate other AutomataAgents as part of the conversation.

## Usage

To use the AutomataAgent, first create an instance of AutomataAgentBuilder, set the desired properties, and then build the agent. You can then run the agent, providing it with tasks and iterating through them until a result is produced or the max iterations are exceeded.

For MasterAutomataAgent, you can create a new instance by converting an existing AutomataAgent using the `from_agent` method. Once you have a MasterAutomataAgent instance, you can set its coordinator using the `set_coordinator` method.

## Examples

### Creating an AutomataAgent

```python
from core.agent.automata_agent_builder import AutomataAgentBuilder

builder = AutomataAgentBuilder()
agent = builder.with_model("gpt-3.5-turbo").with_instructions("Generate a response.").build()
```

### Converting an AutomataAgent to a MasterAutomataAgent

```python
from core.agent.automata_agent import MasterAutomataAgent

master_agent = MasterAutomataAgent.from_agent(agent)
```

### Running the Agent

```python
result = agent.run()
print(result)
```

## References

### AutomataAgent

- `run()`: Runs the agent and iterates through the ›tasks until a result is produced or the max iterations are exceeded.
- `iter_task()`: Executes a single iteration of the task and returns ›the latest assistant and user messages.
- `replay_messages()`: Replays the messages in the conversation and returns the completion message if found.
- `modify_last_instruction(new_instruction: str)`: Modifies the last instruction in the conversation with a new message.
- `get_non_instruction_messages()`: Retrieves all messages in the conversation that are not system instructions.

### MasterAutomataAgent

- `set_coordinator(coordinator: AutomataCoordinator)`: Set the coordinator for the MasterAutomataAgent.
- `from_agent(agent: AutomataAgent)`: Create a MasterAutomataAgent from an existing AutomataAgent.

### AutomataAgentBuilder

- `from_config(config: Optional[AutomataAgentConfig])`: Create an AutomataAgentBuilder instance using the provided configuration object.
- `with_instruction_payload(instruction_payload: Dict[str, str])`: Set the initial payload for the AutomataAgent instance.
- `with_llm_toolkits(llm_toolkits: Dict[ToolkitType, Toolkit])`: Set the low-level manipulation (LLM) toolkits for the AutomataAgent instance.
- `with_instructions(instructions: str)`: Set the instructions for the AutomataAgent instance.
- `with_model(model: str)`: Set the model for the AutomataAgent instance and validate if it is supported.
- `with_stream(stream: bool)`: Set the stream flag for the AutomataAgent instance.
- `with_verbose(verbose: bool)`: Set the verbose flag for the AutomataAgent instance.
- `with_max_iters(max_iters: int)`: Set the maximum number of iterations for the AutomataAgent instance.
- `with_temperature(temperature: float)`: Set the temperature for the AutomataAgent instance.
- `with_session_id(session_id: Optional[str])`: Set the session ID for the AutomataAgent instance.
- `with_eval_mode(eval_mode: bool)`: Set the evaluation mode for the AutomataAgent instance.
- `with_instruction_version(instruction_version: str)`: Set the instruction version for the AutomataAgent instance.
- `build()`: Build and return an AutomataAgent instance with the current configuration.
- `build_master()`: Build and return an MasterAutomataAgent instance with the current configuration.

### AutomataActionExtractor

- `extract_actions(text: str)`: Extract the actions from the given text.

### AutomataAgentHelpers

- `generate_user_observation_message(observations: Dict[str, str], include_prefix: bool)`: Create a formatted message for the user based on the provided observations.
- `append_observation_message(observation_name: str, observations: Dict[str, str], message: str)`: Append an observation message to an existing message.
- `retrieve_completion_message(processed_inputs: Dict[str, str])`: Retrieve a completion message from the processed inputs, if it exists.
- `create_instruction_payload(overview: str, agents_message: str)`: Create an initial payload for the MasterAutomataAgent based on the provided overview and agents_message.

### AutomataActions

- `Action.from_lines(lines: List[str], index: int)`: A factory method to create an instance of an Action subclass from a list of lines and an index.
- `ToolAction.from_lines(lines: List[str], index: int)`: Create a ToolAction instance from a list of lines and an index.
- `AgentAction.from_lines(lines: List[str], index: int)`: Create an AgentAction instance from a list of lines and an index.
- `ResultAction.from_lines(lines: List[str], index: int)`: Create a ResultAction instance from a list of lines and an index.
