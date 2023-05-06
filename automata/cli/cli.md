# Automata Agent CLI Documentation

## Overview

The command line interface (CLI) for the Automata agent provides a simple and convenient way to interact with the agent. This document covers the available commands and options for using the Automata agent CLI.

## Usage

The CLI has two main commands: `master` and `evaluator`. The `master` command is used to launch the master agent, while the `evaluator` command is used to run evaluations for different configurations.

To use the CLI, you need to import the required modules and define the commands with their respective options.

### Common Options

Common options shared by both `master` and `evaluator` commands:

- `--instructions`: The initial instructions for the agent.
- `--model`: The model to use across the framework (default: "gpt-4").
- `--session_id`: The session ID for the agent.
- `--llm_toolkits`: A comma-separated list of toolkits to be used by the master agent (default: "python_indexer,python_writer,codebase_oracle").
- `--master_config_version`: The config version of the agent (default: AgentConfigVersion.AUTOMATA_MASTER_DEV.value).
- `--agent_config_versions`: The config version of the agent (default: AgentConfigVersion.AUTOMATA_INDEXER_DEV.value,AgentConfigVersion.AUTOMATA_WRITER_DEV.value).
- `--stream`: Whether to stream the responses (default: True).
- `-v`/`--verbose`: Execute script in verbose mode (default: False).

### Master Command

To run the `master` command, use the following options:

- `--instruction_version`: The config version of the agent (default: InstructionConfigVersion.AGENT_INTRODUCTION_DEV.value).
- `--include_overview`: Whether the instruction prompt should include an overview (default: False).

Example usage:

```shell
automata master --instructions "Write a Python function" --model gpt-4
```

Example usage:

```shell
automata evaluator  --eval_config "python_indexer_payload"
```

## References

- Automata Agent CLI code: [https://github.com/OpenAI/automata/blob/master/cli.py](https://github.com/OpenAI/automata/blob/master/cli.py)
- Automata Agent Config Enums: [https://github.com/OpenAI/automata/blob/master/configs/config_enums.py](https://github.com/OpenAI/automata/blob/master/configs/config_enums.py)
