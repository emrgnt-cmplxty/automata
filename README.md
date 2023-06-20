# Automata: The Self-Coding Machine

**Automata's objective is to evolve into a fully autonomous, self-programming Artificial Intelligence system**.

This project is inspired by the theory that code is essentially a form of memory, and when furnished with the right tools, AI can evolve real-time capabilities which can potentially lead to the creation of AGI. The word automata comes from the Greek word αὐτόματος, denoting "self-acting, self-willed, self-moving,", and [Automata theory](https://en.wikipedia.org/wiki/Automata_theory) is the study of abstract machines and [automata](https://en.wikipedia.org/wiki/Automaton), as well as the computational problems that can be solved using them.

## Installation and Usage

### Initial Setup

Follow these steps to setup the Automata environment

```bash
# Clone the repository
git clone git@github.com:EmergentAGI/Automata.git
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
MY_API_KEY=your_openai_api_key_here
DB_PATH="$PWD/conversations.sqlite3"
sed -i "s|your_openai_api_key|$MY_API_KEY|" .env
sed -i "s|your_conversation_db_path|$DB_PATH|" .env
```

### Build the docs

How to build the documentation (refreshing is not yet fully formed)

```bash

# Update the code embeddings
automata run-code-embedding

# "L1" docs are the docstrings written into the code

# Build and embed the L2 docs
automata run-doc-embedding-l2

# Build and embed the L3 docs
automata run-doc-embedding-l3
```

### Indexing (Optional)

[SCIP indices](https://about.sourcegraph.com/blog/announcing-scip) are required to run the Automata Interpreter. These indices are used to create the code graph which facilitates search. New indices are generated and uploaded periodically for the Automata Interpreter codebase, but developers must be generate them manually if necessary for their local development. We recommend following the [instructions here](https://github.com/sourcegraph/scip-python).

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
mv index.scip automata/config/symbol/index.scip


### Alternatively, you mean run ./regenerate_index after changing local permissions and completing the above install.
```

Note, this command may result in a buffer overflow error that requires a manual code modification to fix.

---

## Understanding Automata

Automata works by combining Large Language Models, such as GPT-4, with a vector database to form an integrated system capable of documenting, searching, and writing code. The procedure initiates with the generation of comprehensive documentation and code instances. This, coupled with search capabilities, forms the foundation for Automata's self-coding potential.

Automata employs downstream tooling to execute advanced coding tasks, continually building its expertise and autonomy. This self-coding approach mirrors an autonomous craftsman's work, where tools and techniques are consistently refined based on feedback and accumulated experience.

## Hierarchical Operation

Automata operates in a hierarchical structure, where agents at lower levels specialize in specific tasks like generating code snippets or analyzing a document segment. In contrast, higher-level agents supervise lower-level operations, assemble their outputs into a coherent whole, and strategically decide on the project's direction. This system, inspired by human cognition and organization theories, facilitates the emergence of complex behavior from the collaboration of simpler, specialized subsystems.

Automata's design accommodates extensibility, enabling seamless integration with various APIs and libraries to enhance its capabilities. Additionally, it can leverage external data sources and real-time feedback from its interactions to constantly update its knowledge and skills.

## Future

The ultimate goal of the Automata system is to achieve a level of proficiency where it can independently design, write, test, and refine complex software systems. This includes the ability to understand and navigate large codebases, reason about software architecture, optimize performance, and even invent new algorithms or data structures when necessary.

While the complete realization of this goal is likely to be a complex and long-term endeavor, each incremental step towards it not only has the potential to dramatically increase the productivity of human programmers, but also to shed light on fundamental questions in AI and computer science.

## Inspiration and Future Endeavors

Automata was born from the amalgamation of inspiring projects like [Auto-GPT](https://github.com/Significant-Gravitas/Auto-GPT), [BabyAGI](https://github.com/yoheinakajima/babyagi), [AgentGPT](https://github.com/reworkd/AgentGPT), and is designed to inspire many more. We're eager to see what you're building and how we can learn and evolve together in this uncharted AI territory.

## License

Automata is licensed under the Apache License 2.0.
