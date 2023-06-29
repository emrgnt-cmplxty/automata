# Automata: The Future is Self-Written

![Banner](./automata_banner.png)

[![codecov](https://codecov.io/github/emrgnt-cmplxty/Automata/branch/main/graph/badge.svg?token=ZNE7RDUJQD)](https://codecov.io/github/emrgnt-cmplxty/Automata)
[![Documentation Status](https://readthedocs.org/projects/automata/badge/?version=latest)](https://automata.readthedocs.io/en/latest/?badge=latest)
[![Type Checking](https://github.com/emrgnt-cmplxty/Automata/actions/workflows/check-mypy.yml/badge.svg)](https://github.com/emrgnt-cmplxty/Automata/actions/workflows/check-mypy.yml)
[![Discord](https://img.shields.io/discord/1120774652915105934?logo=discord)](https://discord.gg/j9GxfbxqAe)
[![Twitter Follow](https://img.shields.io/twitter/follow/ocolegro?style=social)](https://twitter.com/ocolegro)

**Automata's objective is to evolve into a fully autonomous, self-programming Artificial Intelligence system**.

This project is inspired by the theory that code is essentially a form of memory, and when furnished with the right tools, AI can evolve real-time capabilities which can potentially lead to the creation of AGI. The word automata comes from the Greek word αὐτόματος, denoting "self-acting, self-willed, self-moving,", and [Automata theory](https://en.wikipedia.org/wiki/Automata_theory) is the study of abstract machines and [automata](https://en.wikipedia.org/wiki/Automaton), as well as the computational problems that can be solved using them. More information follows below.

## 🧠 [Read the Docs](https://automata.readthedocs.io/en/latest/)

---

## Demo


https://github.com/emrgnt-cmplxty/Automata/assets/68796651/2e1ceb8c-ac93-432b-af42-c383ea7607d7


<img width="1059" alt="Automata_Rough_Schematic_06_22_23" src="https://github.com/emrgnt-cmplxty/Automata/assets/68796651/57ae3418-c01b-4b3f-a548-2f050c234b34">

---

## Installation and Usage

### Initial Setup

Follow these steps to setup the Automata environment

```bash
## NOTE - the code below is contained in setup.sh.example

# Clone the repository
git clone git@github.com:emrgnt-cmplxty/Automata.git
cd Automata

# Create the local environment
python3 -m venv local_env
source local_env/bin/activate

# Install the project in editable mode
pip3 install -e .

# Setup pre-commit hooks
pre-commit install

# Set up .env
cp .env.example .env
OPEN_API_KEY=your_openai_api_key_here
GITHUB_API_KEY=your_github_api_key
CONVERSATION_DB_PATH="$PWD/conversation_db.sqlite3"
TASK_DB_PATH="$PWD/task_db.sqlite3"
TASKS_OUTPUT_PATH="$PWD/tasks"
REPOSITORY_NAME="emrgnt-cmplxty/Automata"
sed -i "s|your_openai_api_key|$OPEN_API_KEY|" .env
sed -i "s|your_github_api_key|$GITHUB_API_KEY|" .env
sed -i "s|your_conversation_db_path|$CONVERSATION_DB_PATH|" .env
sed -i "s|your_task_db_path|$TASK_DB_PATH|" .env
sed -i "s|your_tasks_output_path|$TASKS_OUTPUT_PATH|" .env
sed -i "s|your_repository_name|$REPOSITORY_NAME|" .env
# Additional Notes -
# Default Max Workers is 8, manually change the .env to update this quantity.
# For MAC users, the example should read as follows -
## sed -i '' "s|your_openai_api_key|$OPEN_API_KEY|" .env

# Fetch the submodules
git submodule update --init --recursive

### NOTE - You must install git-lfs, if you have not done so already

### For Ubuntu, run the following:
##  sudo apt-get install git-lfs
### For Mac, run the following:
##  brew install git-lfs
###
### Then, initialize by running the following:
##  git lfs install
##  git lfs pull
```

### Indexing

[SCIP indices](https://about.sourcegraph.com/blog/announcing-scip) are required to run the Automata Search. These indices are used to create the code graph which relates all dependencies. New indices are generated and uploaded periodically for the Automata Interpreter codebase, but developers must be generate them manually if necessary for their local development. If you encounter issues, we recommending referring to the [instructions here](https://github.com/sourcegraph/scip-python).

```bash
# Activate the local repository
source local_env/bin/activate

# Install scip-python locally
cd scip-python
npm install

# Build the tool
cd packages/pyright-scip
npm run build

# Return to working dir
cd ../../../

# Generate the local index
node scip-python/packages/pyright-scip/index index  --project-name automata --output index_from_fork.scip  --target-only automata

# Copy into the default index location
mv index_from_fork.scip automata/config/symbol/index.scip


### Alternatively, you mean run ./regenerate_index after changing local permissions and completing the above install.
```

### Build the embeddings + docs

The following commands will build the embeddings and docs for the Automata Interpreter codebase. This process can take a while, so we recommend running it in the background.

```bash
# Build/refresh the code embeddings
automata run-code-embedding

# "L1" docs are the docstrings written into the code
# "L2" docs are generated from the L1 docs + symbol context
# Build/refresh and embed the L2 docs
automata run-doc-embedding-l2

# "L3" docs are generated from the L2 docs + symbol context
# Build/refresh and embed the L3 docs
automata run-doc-embedding-l3
```

### Run the system

The following commands illustrate how to run the system with a trivial instruction. It is recommended that your initial run is something of this sort to ensure the system is working as expected.

```bash
# Run a single agent w/ trivial instruction
automata run-agent --instructions="Return true" --model=gpt-3.5-turbo-0613

# Run a single agent w/ a non-trivial instruction
automata run-agent --instructions="Explain what AutomataAgent is and how it works, include an example to initialize an instance of AutomataAgent." --model=gpt-3.5-turbo-16k
```

---

## Understanding Automata

Automata works by combining Large Language Models, such as GPT-4, with a vector database to form an integrated system capable of documenting, searching, and writing code. The procedure initiates with the generation of comprehensive documentation and code instances. This, coupled with search capabilities, forms the foundation for Automata's self-coding potential.

Automata employs downstream tooling to execute advanced coding tasks, continually building its expertise and autonomy. This self-coding approach mirrors an autonomous craftsman's work, where tools and techniques are consistently refined based on feedback and accumulated experience.

### Example - Running your own agent

Sometimes the best way to understand a complicated system is to start by understanding a basic example. The following example illustrates how to run your own Automata agent. The agent will be initialized with a trivial instruction, and will then attempt to write code to fulfill the instruction. The agent will then return the result of its attempt.

```python

import logging
from automata.config.openai_agent import AutomataOpenAIAgentConfigBuilder
from automata.core.agent.providers import OpenAIAutomataAgent
<<<<<<< HEAD
from automata.core.agent.tool.tool_utils import AgentToolFactory, dependency_factory
=======
from automata.core.agent.tool.tool_utils import AgentToolFactory, DependencyFactory
>>>>>>> 8d9b696 (rename files for style clarity)
from automata.core.coding.py.module_loader import py_module_loader

logger = logging.getLogger(__name__)

# Initialize the module loader to the local directory
py_module_loader.initialize()

# Construct the set of all dependencies that will be used to build the tools
toolkit_list = ["context-oracle"]
tool_dependencies = dependency_factory.build_dependencies_for_tools(toolkit_list)

# Build the tools
tools = AgentToolFactory.build_tools(toolkit_list, **tool_dependencies)

# Build the agent config
agent_config = (
    AutomataOpenAIAgentConfigBuilder.from_name("automata-main")
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
from automata.core.symbol.base import SymbolCodeEmbedding
from automata.core.symbol.parser import parse_symbol

symbol_str = 'scip-python python automata 75482692a6fe30c72db516201a6f47d9fb4af065 `automata.core.agent.agent_enums`/ActionIndicator#'
symbol = parse_symbol(symbol_str)
source_code = 'symbol_source'
vector = np.array([1, 0, 0, 0])

embedding = SymbolCodeEmbedding(symbol=symbol, source_code=source_code, vector=vector)
```

Code example for creating an instance of 'SymbolDocEmbedding':
```python
from automata.core.symbol.base import SymbolDocEmbedding
from automata.core.symbol.parser import parse_symbol
import numpy as np

symbol = parse_symbol('your_symbol_here')
document = 'A document string containing information about the symbol.'
vector = np.random.rand(10)

symbol_doc_embedding = SymbolDocEmbedding(symbol, document, vector)
```

</details>

## SymbolRank

We have developed SymbolRank for Automata, a semantic code analyzer for software corpora. Leveraging language models and graph theory, SymbolRank assesses and ranks symbols such as classes and methods based on their semantic context and structural relationships within the software. The algorithm starts by embedding a global context using a concrete implementation of the SymbolEmbeddingHandler class, which applies OpenAI's API to generate vector representations of each symbol in the source code. These embeddings capture the semantic essence of the symbols, providing a basis for the subsequent stages of the process.

Simultaneously, the software corpus is used to construct a SymbolGraph. Each symbol in the corpus becomes a node in this graph, with dependencies between symbols forming the edges. The graph provides a comprehensive map of structural information in the codebase, offering methods to understand symbol dependencies, relationships, callers, and callees, and the ability to produce a rankable subgraph of symbols.

The SymbolRank class then uses a prepared similarity dictionary for a given query and the SymbolGraph. The algorithm subsequently executes an iterative computation akin to Google's PageRank, but considers both the symbols' similarity scores to the query and their connectivity within the graph. This amalgamation of natural language processing, information retrieval, and graph theory methods results in a ranking of code symbols, significantly aiding tasks like code understanding, navigation, recommendation, and search.

## Hierarchical Operation

Automata operates in a hierarchical structure, where providers at lower levels specialize in specific tasks like generating code snippets or analyzing a document segment. In contrast, higher-level providers supervise lower-level operations, assemble their outputs into a coherent whole, and strategically decide on the project's direction. This system, inspired by human cognition and organization theories, facilitates the emergence of complex behavior from the collaboration of simpler, specialized subsystems.

Automata's design accommodates extensibility, enabling seamless integration with various APIs and libraries to enhance its capabilities. Additionally, it can leverage external data sources and real-time feedback from its interactions to constantly update its knowledge and skills.

## Future

The ultimate goal of the Automata system is to achieve a level of proficiency where it can independently design, write, test, and refine complex software systems. This includes the ability to understand and navigate large codebases, reason about software architecture, optimize performance, and even invent new algorithms or data structures when necessary.

While the complete realization of this goal is likely to be a complex and long-term endeavor, each incremental step towards it not only has the potential to dramatically increase the productivity of human programmers, but also to shed light on fundamental questions in AI and computer science.

## Inspiration and Future Endeavors

Automata was born from the amalgamation of inspiring projects like [Auto-GPT](https://github.com/Significant-Gravitas/Auto-GPT), [BabyAGI](https://github.com/yoheinakajima/babyagi), [AgentGPT](https://github.com/reworkd/AgentGPT), and [GPT-Engineer](https://github.com/AntonOsika/gpt-engineer) and is designed to inspire many more. We're eager to see what you're building and how we can learn and evolve together in this uncharted AI territory.

## License

Automata is licensed under the Apache License 2.0.

## Other

This project is an extension of an initial effort between [emrgnt-cmplxty](https://github.com/emrgnt-cmplxty) and [maks-ivanov](https://github.com/maks-ivanov) that began with this [repository](https://github.com/maks-ivanov/automata).
