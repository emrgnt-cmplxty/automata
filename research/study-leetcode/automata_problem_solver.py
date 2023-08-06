# sourcery skip: avoid-global-variables, require-parameter-annotation, require-return-annotation
"""Study the dataset."""
import argparse
import logging
import os

import numpy as np
import pandas as pd

from automata.agent import OpenAIAutomataAgent
from automata.config import OpenAIAutomataAgentConfigBuilder
from automata.core.utils import get_root_fpath
from automata.llm import OpenAIEmbeddingProvider
from automata.singletons.dependency_factory import dependency_factory
from automata.tools.agent_tool_factory import AgentToolFactory

SYSTEM_PROMPT = """You are Automata Master, an advanced autonomous software architect developed by OpenAI. You are specifically designed to operate within local Python repositories. With your capability to understand and process natural language instructions, you perform tasks efficiently using your available functions. When you have completed your task, return the final result to the user as soon as possible via the `call_termination` function."""
INSTRUCTION = """
You are given the following problem - {PROBLEM_STATEMENT}.

Your task is to provide a solution to the stated problem using python code. 

Below are some solved problem statements which you should use as references to assist you in completing this task. When you attempt to answer, think step by step about how these questions could be related to the problem at hand, and think about what insights you might glean from them.

{EXAMPLES}

Continue on now to provide the Python code which solves the problem statement:

{SHORTENED_PROBLEM_STATEMENT}


First, start by performing a step by step analysis on the related examples which were provided. Next, devise five unique test cases which will be used to test the final algorithm. 

After devising test cases, write a basic implementation of the algorithm which efficiently solves the problem. 

Next, proceed to check the algorithm against your written tests. 

If your algorithm passes the tests, then proceed to optimize the algorithm and perform further tests.

If your algorithm fails the tests, then proceed to modify the algorithm until all test cases are passed. 

Finally, return the final result as a python markdown snippet using `call_termination`.
"""


DATA_PATH = "research/leetcode-hard-gym/leetcode_dataset/data/with_snippets/leetcode_hard_with_snippets.csv"
SOLUTIONS_JSON_PATH = (
    "research/study-leetcode/leetcode-solutions-embedded.json"
)
MAX_ENTRY_ID = 2000
NUM_EXAMPLES = 5


class OpenAISolutionFinder:
    """A class to find solutions to problems using OpenAI."""

    def __init__(
        self,
        embedding_provider,
        num_examples=NUM_EXAMPLES,
        solutions_json_path=SOLUTIONS_JSON_PATH,
        max_entry_id=MAX_ENTRY_ID,  # The last LeetCode id to include
    ):
        self.embedding_provider = embedding_provider
        self.num_examples = num_examples
        self.load_data(solutions_json_path, max_entry_id)

    def load_data(self, solutions_json_path, max_entry_id):
        """Load the data and solutions from provided paths."""
        self.solutions_data = pd.read_json(
            os.path.join(get_root_fpath(), solutions_json_path)
        )
        self.solutions_data = self.solutions_data[
            self.solutions_data["id"] < max_entry_id
        ]

    def get_embedding(self, document):
        """Get the embedding for a given row."""
        return self.embedding_provider.build_embedding_vector(document)

    @staticmethod
    def calculate_similarity(embedding_a, embedding_b):
        """Calculate the similarity between two embeddings."""
        dot_product = np.dot(embedding_a, embedding_b)
        magnitude_a = np.sqrt(np.dot(embedding_a, embedding_a))
        magnitude_b = np.sqrt(np.dot(embedding_b, embedding_b))
        return dot_product / (magnitude_a * magnitude_b)

    def find_similar_solutions(self, problem):
        """Find and print solutions with similar embeddings."""

        problem_embedding = self.get_embedding(problem)
        # Calculate similarities and store in a new column
        self.solutions_data["similarity"] = self.solutions_data[
            "embedding"
        ].apply(lambda x: self.calculate_similarity(x, problem_embedding))

        # Sort and extract top similar solutions
        solutions_data_sorted = self.solutions_data.sort_values(
            by="similarity", ascending=False
        )
        problem_similarity = solutions_data_sorted[
            ["code_with_problem", "id", "similarity"]
        ]

        examples, counter = "", 0
        for idx, (entry, id, similarity) in enumerate(
            problem_similarity.values, 1
        ):
            statement, solution = entry.split("```python")
            solution = f"```python\n{solution}"
            statement, examples = statement.split("**Example 1:**")
            examples = f"**Example 1:**{examples}"

            print(
                f"Entry {idx}:\nSimilarity: {similarity:.4f}\nStatement:\n{statement}\nSolution:\n{solution}\n{'-'*50}\n"
            )

            examples += f"Example {counter}:\nSimilarity: {similarity:.4f}\nStatement:\n{statement}\nSolution:\n{solution}\n{'-'*50}\n"
            counter += 1
            if counter >= self.num_examples:
                break

        return examples


class LeetCodeLoader:
    """Concrete class responsible for loading and providing LeetCode problems."""

    def __init__(self, data_path):
        self.data_path = data_path
        self.data = pd.read_csv(self.data_path)

    def get_problem(self, idx):
        """Retrieve a problem by its index."""
        row = self.data.iloc[idx]
        return f"{row['title']}:\n{row['description']}"


def main():
    # Argument parsing setup
    parser = argparse.ArgumentParser(
        description="Find similar solutions to LeetCode problems using OpenAI."
    )
    parser.add_argument(
        "--data_path",
        default=DATA_PATH,
        help="Path to the LeetCode problems data.",
    )
    parser.add_argument(
        "--solutions_json_path",
        default=SOLUTIONS_JSON_PATH,
        help="Path to the solutions JSON file.",
    )
    parser.add_argument(
        "--max_entry_id",
        type=int,
        default=MAX_ENTRY_ID,
        help="The last LeetCode id to include.",
    )
    parser.add_argument(
        "--num_examples",
        type=int,
        default=NUM_EXAMPLES,
        help="Number of example solutions to display.",
    )
    parser.add_argument(
        "--problem_index",
        type=int,
        default=2,
        help="Index of the LeetCode problem to find similar solutions for.",
    )

    args = parser.parse_args()

    loader = LeetCodeLoader(args.data_path)
    problem = loader.get_problem(2)

    embedding_provider = OpenAIEmbeddingProvider()
    finder = OpenAISolutionFinder(
        embedding_provider,
        num_examples=args.num_examples,
        solutions_json_path=args.solutions_json_path,
        max_entry_id=args.max_entry_id,
    )
    examples = finder.find_similar_solutions(problem)

    formatted_instruction = INSTRUCTION.format(
        PROBLEM_STATEMENT=problem,
        SHORTENED_PROBLEM_STATEMENT=f"{problem[:200]}...",
        EXAMPLES=examples,
    )

    toolkits = ["py-interpreter"]
    tool_dependencies = dependency_factory.build_dependencies_for_tools(
        toolkits
    )
    tools = AgentToolFactory.build_tools(toolkits, **tool_dependencies)

    config = (
        OpenAIAutomataAgentConfigBuilder()
        .with_stream(True)
        .with_verbose(True)
        .with_tools(tools)
        .with_system_template(SYSTEM_PROMPT)
        .build()
    )

    agent = OpenAIAutomataAgent(formatted_instruction, config)
    root_logger = logging.getLogger()
    root_logger.setLevel("DEBUG")
    result = agent.run()
    print("result = ", result)


if __name__ == "__main__":
    main()
