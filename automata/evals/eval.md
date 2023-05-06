# Eval Class Documentation

## Overview

The Eval class is a base class for evaluating the performance of an AutomataAgent given a set of instructions. It provides methods for generating evaluation results and extracting actions from the agent's responses. Subclasses of the Eval class should override the eval_sample and run methods to customize evaluation behavior.

## Usage

To use the Eval class, first create an instance of the class with the required agent_config parameter and any optional keyword arguments. Then, call the generate_eval_result method with an instruction and a list of expected actions to evaluate the agent's performance.

## Examples

### Creating an Eval Instance

```python
from automata.evals.eval import Eval
from automata.configs.config_enums import AgentConfigVersion

evaluator = Eval(
    agent_config=AutomataAgentConfig.load(AgentConfigVersion.AUTOMATA_INDEXER_DEV),
    llm_toolkits=args.llm_toolkits,
    model=args.model,
    instruction_payload=instruction_payload,
    stream=args.stream,
)
```

### Generating an Eval Result

```python
eval_result = evaluator.generate_eval_result(instruction, expected_actions)
```

## References

### Eval

`**init**(self, *args, **kwargs)`: Initializes an Eval object with the following optional keyword arguments:

`agent_config`: Configuration for the AutomataAgentBuilder (required).

`instruction_payload`: Instruction payload for the AutomataAgentBuilder.

`model`: Model to use for the agent.
session_id: Session ID for the agent.
stream: Stream for the agent.
with_max_iters: Maximum number of iterations for the agent.
llm_toolkits: Low-level model toolkits for the agent.
with_master: Option to use the master model.
generate_eval_result(self, instruction: str, expected_actions: List[EvalAction]) -> EvalResult: Evaluates a single sample by constructing an agent using the provided instruction, running the agent, extracting the actions performed by the agent, and comparing them to the expected_actions. Returns an EvalResult object with the evaluation results.
\_extract_actions(messages: List[OpenAIChatMessage]) -> List[Action]: A static method that extracts a list of Action objects from a list of OpenAIChatMessage objects.

### Helper Classes and Functions

### EvalResult

A class to represent the result of an evaluation.
Contains the following attributes:
token_match: A boolean indicating whether there was a token match between expected and extracted actions.
full_match: A boolean indicating whether there was a full match between expected and extracted actions.
EvalAction
A class to represent an action in an evaluation. Contains the following methods:
token_match(self, action_str: str) -> bool: Performs a relative comparison between an action string and the action's tokens.
full_match(self, extracted_action: Action, expected_action: Action) -> bool: Performs an exact comparison between two actions.
calc_eval_result
calc_eval_result(extracted_actions: List[Action], expected_actions: List[EvalAction]) -> EvalResult: A function that calculates the evaluation result based on the extracted actions and expected actions, returning an EvalResult object.
