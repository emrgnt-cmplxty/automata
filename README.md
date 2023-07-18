# Automata: The Future is Self-Written

![Banner](https://github.com/emrgnt-cmplxty/Automata/assets/68796651/61fe3c33-9b7a-4c1b-9726-a77140476b83)

[![codecov](https://codecov.io/github/emrgnt-cmplxty/Automata/branch/main/graph/badge.svg?token=ZNE7RDUJQD)](https://codecov.io/github/emrgnt-cmplxty/Automata)
[![CodeFactor](https://www.codefactor.io/repository/github/emrgnt-cmplxty/automata/badge)](https://www.codefactor.io/repository/github/emrgnt-cmplxty/automata)
  <a href="https://github.com/emrgnt-cmplxty/automata/blob/main/LICENSE" target="_blank">
      <img src="https://img.shields.io/static/v1?label=license&message=Apache 2.0&color=white" alt="License">
  </a> 
[![Documentation Status](https://readthedocs.org/projects/automata/badge/?version=latest)](https://automata.readthedocs.io/en/latest/?badge=latest)
[![GitHub star chart](https://img.shields.io/github/stars/emrgnt-cmplxty/Automata?style=social)](https://star-history.com/#emrgnt-cmplxty/Automata)
[![Discord](https://img.shields.io/discord/1120774652915105934?logo=discord)](https://discord.gg/j9GxfbxqAe)
[![Twitter Follow](https://img.shields.io/twitter/follow/ocolegro?style=social)](https://twitter.com/ocolegro)


[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/emrgnt-cmplxty/Automata)

**Automata's objective is to evolve into a fully autonomous, self-programming Artificial Intelligence system**.

This project is inspired by the theory that code is essentially a form of memory, and when furnished with the right tools, AI can evolve real-time capabilities which can potentially lead to the creation of AGI. The word automata comes from the Greek word αὐτόματος, denoting "self-acting, self-willed, self-moving,", and [Automata theory](https://en.wikipedia.org/wiki/Automata_theory) is the study of abstract machines and [automata](https://en.wikipedia.org/wiki/Automaton), as well as the computational problems that can be solved using them. More information follows below.

---

## Demo

https://github.com/emrgnt-cmplxty/Automata/assets/68796651/2e1ceb8c-ac93-432b-af42-c383ea7607d7

## Rough Schematic

<p align="center">
    <img width="971" alt="Rough_Schematic_06_30_23_" src="https://github.com/emrgnt-cmplxty/Automata/assets/68796651/f73f37ac-6335-4066-b9bc-79f9a2652cc1">
</p>

---

## Installation and Usage

### 🧠 [Stuck? Try the Docs](https://automata.readthedocs.io/en/latest/)

### Initial Setup

Follow these steps to setup the Automata environment

```bash
# Clone the repository
git clone git@github.com:emrgnt-cmplxty/Automata.git && cd Automata/

# Install dependencies
poetry install

# Configure the environment and setup files
automata configure
```

### Indexing

[SCIP indices](https://about.sourcegraph.com/blog/announcing-scip) are required to run the Automata Search. These indices are used to create the code graph which relates symbols by dependencies across the codebase. New indices are generated and uploaded periodically for the Automata codebase, but programmers must be generate them manually if necessary for their local development. If you encounter issues, we recommend referring to the [instructions here](https://github.com/sourcegraph/scip-python).

```bash
# Make sure you are in /scripts
# Install dependencies and run indexing on the local codebase
./install_indexing.sh && ./regenerate_index.sh
```

### Build the embeddings + docs

The following commands will build the embeddings and docs for the Automata Interpreter codebase. This process can take a while, so we recommend running it in the background.

```bash
# Build/refresh the code embeddings
automata run-code-embedding

# "L1" docs are the docstrings written into the code
# "L2" docs are generated from the L1 docs + symbol context
automata run-doc-embedding --embedding-level 2

# "L3" docs are generated from the L2 docs + symbol context
automata run-doc-embedding --embedding-level 3
```

### Run the system

The following commands illustrate how to run the system with a trivial instruction. It is recommended that your initial run is something of this sort to ensure the system is working as expected.

```bash
# Run a single agent w/ trivial instruction
automata run-agent --instructions="Return true" --model=gpt-3.5-turbo-0613

# Run a single agent w/ a non-trivial instruction
automata run-agent --instructions="Explain what AutomataAgent is and how it works, include an example to initialize an instance of AutomataAgent."
```

---

## Understanding Automata

Automata works by combining Large Language Models, such as GPT-4, with a vector database to form an integrated system capable of documenting, searching, and writing code. The procedure initiates with the generation of comprehensive documentation and code instances. This, coupled with search capabilities, forms the foundation for Automata's self-coding potential.

Automata employs downstream tooling to execute advanced coding tasks, continually building its expertise and autonomy. This self-coding approach mirrors an autonomous craftsman's work, where tools and techniques are consistently refined based on feedback and accumulated experience.

### Example - Building your own agent

Sometimes the best way to understand a complicated system is to start by understanding a basic example. The following example illustrates how to run your own Automata agent. The agent will be initialized with a trivial instruction, and will then attempt to write code to fulfill the instruction. The agent will then return the result of its attempt.

```python

from automata.config.base import AgentConfigName, OpenAIAutomataAgentConfigBuilder
from automata.agent import OpenAIAutomataAgent
from automata.singletons.dependency_factory import dependency_factory
from automata.singletons.py_module_loader import py_module_loader
from automata.tools.factory import AgentToolFactory

# Initialize the module loader to the local directory
py_module_loader.initialize()

# Construct the set of all dependencies that will be used to build the tools
toolkit_list = ["context-oracle"]
tool_dependencies = dependency_factory.build_dependencies_for_tools(toolkit_list)

# Build the tools
tools = AgentToolFactory.build_tools(toolkit_list, **tool_dependencies)

# Build the agent config
agent_config = (
    OpenAIAutomataAgentConfigBuilder.from_name("automata-main")
    .with_tools(tools)
    .with_model("gpt-4")
    .build()
)

# Initialize and run the agent
instructions = "Explain how embeddings are used by the codebase"
agent = OpenAIAutomataAgent(instructions, config=agent_config)
result = agent.run()
```

<details>
<summary>Click to see the output</summary>

Embeddings in this codebase are represented by classes such as `SymbolCodeEmbedding` and `SymbolDocEmbedding`. These classes store information about a symbol and its respective embeddings which are vectors representing the symbol in high-dimensional space.

Examples of these classes are:
`SymbolCodeEmbedding` a class used for storing embeddings related to the code of a symbol.
`SymbolDocEmbedding` a class used for storing embeddings related to the documentation of a symbol.

Code example for creating an instance of 'SymbolCodeEmbedding':

```python
import numpy as np
from automata.symbol_embedding.base import SymbolCodeEmbedding
from automata.symbol.parser import parse_symbol

symbol_str = 'scip-python python automata 75482692a6fe30c72db516201a6f47d9fb4af065 `automata.agent.agent_enums`/ActionIndicator#'
symbol = parse_symbol(symbol_str)
source_code = 'symbol_source'
vector = np.array([1, 0, 0, 0])

embedding = SymbolCodeEmbedding(symbol=symbol, source_code=source_code, vector=vector)
```

Code example for creating an instance of 'SymbolDocEmbedding':

```python
from automata.symbol_embedding.base import SymbolDocEmbedding
from automata.symbol.parser import parse_symbol
import numpy as np

symbol = parse_symbol('your_symbol_here')
document = 'A document string containing information about the symbol.'
vector = np.random.rand(10)

symbol_doc_embedding = SymbolDocEmbedding(symbol, document, vector)
```

</details>

## Contribution guidelines

**If you want to contribute to Automata, be sure to review the
[contribution guidelines](CONTRIBUTING.md). This project adheres to Automata's
[code of conduct](CODE_OF_CONDUCT.md). By participating, you are expected to
uphold this code.**

**We use [GitHub issues](https://github.com/emrgnt-cmplxty/automata/issues) for
tracking requests and bugs, please see
[Automata Discussions](https://github.com/emrgnt-cmplxty/Automata/discussions/) for general questions and
discussion, and please direct specific questions.**

The Automata project strives to abide by generally accepted best practices in
open-source software development.

## Future

The ultimate goal of the Automata project is to achieve a level of proficiency where it can independently design, write, test, and refine complex software systems. This includes the ability to understand and navigate large codebases, reason about software architecture, optimize performance, and even invent new algorithms or data structures when necessary.

While the complete realization of this goal is likely to be a complex and long-term endeavor, each incremental step towards it not only has the potential to dramatically increase the productivity of human programmers, but also to shed light on fundamental questions in AI and computer science.

## License

Automata is licensed under the Apache License 2.0.

## Other

This project is an extension of an initial effort between [emrgnt-cmplxty](https://github.com/emrgnt-cmplxty) and [maks-ivanov](https://github.com/maks-ivanov) that began with this [repository](https://github.com/maks-ivanov/automata).