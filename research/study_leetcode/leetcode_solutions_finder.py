"""Finds issues from the associated leetcode solutions store"""
import ast
import logging
from typing import Optional

import numpy as np
import pandas as pd
import tiktoken
from constants import DIFFICULTIES, MAX_TOKENS

from automata.agent import OpenAIAutomataAgent
from automata.config import OpenAIAutomataAgentConfigBuilder

logger = logging.getLogger(__name__)


class LeetCodeSolutionsFinder:
    """A class to find example solutions using OpenAI."""

    def __init__(
        self,
        embedding_provider,
        max_entry_id,
        max_num_examples,
        num_examples_to_screen,
        solutions_data_path,
        lowest_difficulty,
    ) -> None:  # sourcery skip: docstrings-for-functions
        self.embedding_provider = embedding_provider
        self.max_num_examples = max_num_examples
        self.num_examples_to_screen = num_examples_to_screen
        self.available_difficulties = DIFFICULTIES
        self.allowed_difficulties = self.available_difficulties[
            self.available_difficulties.index(lowest_difficulty) :
        ]
        self.load_data(solutions_data_path, max_entry_id)

    def load_data(self, solutions_data_path: str, max_entry_id: int) -> None:
        """Load the data and solutions from provided path."""
        self.solutions_data = pd.read_json(solutions_data_path)
        self.solutions_data = self.solutions_data[
            self.solutions_data["id"] < max_entry_id
        ]

        # Extract the difficulties for each provided problem
        difficulty = []
        for entry in self.solutions_data["code_with_data"].values:
            split_entry = entry.split("\n")
            found_match = False
            for line in split_entry:
                if any(
                    f"# {entry}" in line
                    for entry in self.available_difficulties
                ):
                    difficulty.append(line.split("# ")[1])
                    found_match = True
                    break
            if not found_match:
                difficulty.append("Easy")

        # Check that allowed_difficulties are in the 'code_with_data' column
        # for each entry
        self.solutions_data["difficulty"] = difficulty
        self.solutions_data = self.solutions_data[
            self.solutions_data["difficulty"].isin(self.allowed_difficulties)
        ]

    def get_embedding(self, document: str) -> np.ndarray:
        """Get the embedding for a given row."""
        return self.embedding_provider.build_embedding_vector(document)

    @staticmethod
    def calculate_similarity(
        embedding_a: np.ndarray, embedding_b: np.ndarray
    ) -> np.ndarray:
        """Calculate the similarity between two embeddings."""

        dot_product = np.dot(embedding_a, embedding_b)
        magnitude_a = np.sqrt(np.dot(embedding_a, embedding_a))
        magnitude_b = np.sqrt(np.dot(embedding_b, embedding_b))
        return dot_product / (magnitude_a * magnitude_b)

    def find_best_solution_and_explanation(
        self, problem: str
    ) -> Optional[str]:
        """Find and print solutions with similar embeddings."""
        print("problem = ", problem)
        problem_embedding = self.get_embedding(problem)

        # Calculate similarities between solution embeddings and latest problem
        # and store in a new column
        self.solutions_data["similarity"] = self.solutions_data[
            "embedding"
        ].apply(lambda x: self.calculate_similarity(x, problem_embedding))

        # Sort solutions by similarity
        solutions_data_sorted = self.solutions_data.sort_values(
            by="similarity", ascending=False
        )

        examples, counter = [], 0
        for code_with_problem in solutions_data_sorted[
            "code_with_problem"
        ].values:
            statement, solution = code_with_problem.split("```python")
            solution = f"```python\\n{solution}"
            statement, _ = statement.split("**Example 1:**")

            examples.append(
                f"Related Solution {counter}:\nStatement:\n{statement}\nSolution:\n{solution}\n{'-'*50}\n"
            )

            counter += 1
            if counter >= self.num_examples_to_screen:
                break

        encoding = tiktoken.encoding_for_model("gpt-4")
        examples_formatted = "\n".join(examples)
        examples_tokens_consumed = len(encoding.encode(examples_formatted))

        # truncate the examples if they are exceeding our available context
        examples_formatted = examples_formatted[
            : min(
                int(
                    MAX_TOKENS
                    / examples_tokens_consumed
                    * 0.9
                    * len(examples_formatted)
                ),
                len(examples_formatted),
            )
        ]

        logging.info(
            f"Tokens consumed (after reduction) = {examples_tokens_consumed}"
        )

        formatted_instruction = f"Your are given the following problem as context - {problem} \n. Your task is to select at most {self.max_num_examples}, or None, of the following shown Related Solutions, which when combined together provide the best context to help with solving the previously presented problem:\n{examples_formatted}\nYour selected Related Solutions will be forwarded on as additional context to a programmer whose task is to write a solution to the originally given problem. Try to select more difficult solutions, as the stated problem is quite difficult. Return the final result as a simple array of integers, like [12,3,0,1,5]."

        config = (
            OpenAIAutomataAgentConfigBuilder()
            .with_stream(True)
            .with_verbose(False)
            .with_tools([])
            .with_system_template(
                "You are Automata Master, an advanced autonomous software architect developed by OpenAI. You are specifically designed to operate within local Python repositories. With your capability to understand and process natural language instructions, you perform tasks efficiently using your available functions. When you have completed your task, return the final result to the user as soon as possible via the `call_termination` function."
            )
            .build()
        )

        try:
            logging.info("Attempting to fetch the best examples now...")
            agent = OpenAIAutomataAgent(formatted_instruction, config)
            result = agent.run()

            extracted_result = result.split("[")[1].split("]")[0]
            selected = ast.literal_eval(
                f"[{extracted_result}]"
            )  # an integer array like [0, 5, ...]
        except Exception as e:
            logger.error(
                f"An error {e} occurred while selecting the best examples"
            )
            selected = [0, 1, 2]

        return "\n".join(
            [ele for it, ele in enumerate(examples) if it in selected]
        )
