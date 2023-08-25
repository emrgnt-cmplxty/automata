# Zero-Shot Replication Framework

## Overview

The Zero-Shot Replication Framework is a minimal environment designed to replicate zero-shot results from past academic papers. It currently supports OpenAI, Anthropic, and HuggingFace models to generate completions for various datasets and provides tools for handling, evaluating, and storing these completions.

## Results (all models accessed on 08/24-8/25, 2023)

| Category             | gpt-3.5-turbo-0301 | gpt-3.5-turbo-0613 | claude-2 | gpt-4-0314 | gpt-4-0613 | gpt-4 Baseline | Sources  |
|----------------------|--------------------|--------------------|----------|------------|------------|----------------|----------|
| HumanEval            | 67.0               | 61.5               | 65.2     | 86.0       | 84.1       | 67             | [1]      |
| EvalPlus             | 59.1               | 54.2               | 54.9     | 80.5       | 74.4       | N/A            |          |
| GSM8K                | 71.1               | 67.6               | 26.2     | 90.4       | 91.0       | 87.1           |          |

<!-- | LeetCode_100 Easy    | 83.0               | 80.0               | 73.0     | 91.0       | 88.0       | 72.2-75.6      | [1,2]    |
| LeetCode_100 Medium  | 16.0               | 16.0               | 16.0     | 26.0       | 21.0       | 26.2-38.7      | [1,2]    |
| LeetCode_100 Hard    | 1.0                | 3.0                | 2.0      | 6.0        | 6.0        | 6.7-7          | [1,2]    | -->
<!-- | MATH                 | XX                 | XX                 | XX       | XX         | XX         | XX             | [3]      | -->

## Features

- Easy configuration of models and parameters.
- Ability to choose datasets to run on.
- Extensibility through a pluggable problem generator.

## Requirements

- Python >= 3.10 and < 3.12
- Poetry for package management

## Min. Dependencies

- anthropic: "0.3.10"
- astunparse: "1.6.3"
- black: ^23.3.0
- evalplus: ^0.1.6
- numpy: "^1.25.2"
- openai: 0.27.8
- pandas: ^2.0.3
- python-dotenv: ^1.0.0
- python-leetcode: "1.2.1"

# HF Dependencies

- transformers: "^4.32.0"
- torch: "1.13.1"
- accelerate: "^0.22.0"
- sentencepiece: "^0.1.99"
- protobuf: "^4.24.1"

## Dev Dependencies

- flake8: "6.1.0"
- isort: "5.12.0"
- mypy: "^1.5.1"
- pre-commit: "^3.3.3"
- sourcery: "^1.6.0"
- types-requests: "^2.31.0.2"
- types-attrs: "^19.1.0"
- yapf: "0.40.1"

## Installation

Make sure you have [Poetry](https://python-poetry.org/) installed, then clone the repository and install the dependencies.

```bash
git clone https://github.com/your-username/zero-shot-replication.git
cd zero-shot-replication
git submodule update --init --recursive
poetry install
cp .env.example .env # Copy the example environment file
# Edit the .env file to add your OpenAI API key, etc.


# Optional

# If developing, install the pre-commit hooks
pre-commit install 

```

## Usage

You can run the zero-shot replication by executing the `runner.py` file with various command-line arguments.

```bash
poetry run python runner.py --provider openai --dataset human-eval --model gpt-4-0613 --temperature 0.7
```

### Command-Line Arguments

- `--provider`: Which provider to use for zero-shot completions (default: "openai").
- `--dataset`: Which dataset to run on (default: "human-eval").
- `--model`: Model name to load from the provider (default: "gpt-3.5-turbo").
- `--temperature`: Temperature parameter for the provided model (default: 0.7).
- `--output_file_name`: Filename to override the default output file name with.

To see explicit commands ran to generate the reported results, check out the [commands.md](commands.md) menu.

## License

This project is licensed under the Apache-2.0 License.

## Sources

[1] [GPT-4 Technical Report](https://arxiv.org/abs/2303.08774)

[2] [Sparks of Artificial General Intelligence](https://arxiv.org/pdf/2303.12712.pdf)

[3] [Solving Challenging Math Word Problems Using GPT-4 Code Interpreter with Code-based Self-Verification](https://paperswithcode.com/paper/solving-challenging-math-word-problems-using)