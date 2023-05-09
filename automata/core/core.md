# Automata Core Module Documentation

This documentation covers the core module of the Automata codebase, including the core.utils file, which contains utility functions used throughout the project.

## Overview

The core module consists of various components that are essential for the functioning of the Automata Agent. It includes the AutomataAgent, AutomataCoordinator, AutomataActions, and various utility functions. This module is responsible for managing the execution of instructions, interactions with various tools, and managing multiple AutomataInstances.

## core.utils

The core.utils file contains utility functions that are used throughout the Automata codebase. Functions included in this file are:

- `format_prompt()`: Format expected strings into the config.
- `root_py_path()`: Returns the path to the root of the project Python code. Returns a path object in string form.
- `load_config(file_path: str)`: Loads a config file. Takes the path to the YAML file as an argument and returns the content of the YAML file as a Python object.
- `root_path()`: Returns the path to the root of the project directory. Returns a path object in string form.
- `get_logging_config()`: Returns logging configuration.
- `run_retrieval_chain_with_sources_format(chain: BaseConversationalRetrievalChain, q: str)`: Runs a retrieval chain and formats the result with sources. Takes the retrieval chain to run and the query to pass to the retrieval chain as arguments. Returns the formatted result containing the answer and sources.
- `calculate_similarity()`: Calculate the similarity between two strings.

## Examples

### Load a YAML configuration file

```python
from core.utils import load_config

config_file = "path/to/config.yaml"
config = load_config(config_file)
```

### Calculate the similarity between two strings

```python
from core.utils import calculate_similarity

string1 = "Hello, world!"
string2 = "Hello, Automata!"

similarity = calculate_similarity(string1, string2)
print(similarity)
```

## References

- core.utils
  - format_prompt
  - root_py_path
  - load_config
  - root_path
  - get_logging_config
  - run_retrieval_chain_with_sources_format
  - calculate_similarity
