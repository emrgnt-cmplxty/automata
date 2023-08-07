# sourcery skip: avoid-global-variables, require-parameter-annotation, require-return-annotation
# flake8: noqa
"""Study the dataset."""
import argparse
import ast
import os
import sys
import textwrap

import numpy as np
import pandas as pd

from automata.agent import OpenAIAutomataAgent
from automata.cli.commands import configure_logging
from automata.config import OpenAIAutomataAgentConfigBuilder
from automata.core.utils import get_root_fpath
from automata.llm import OpenAIEmbeddingProvider
from automata.singletons.dependency_factory import dependency_factory
from automata.tools.agent_tool_factory import AgentToolFactory

# Get the absolute path of the parent directory
parent_dir = os.path.join(
    get_root_fpath(), "research", "leetcode-hard-gym"  # , "leetcode_env"
)

# Add the parent directory to the PYTHONPATH
sys.path.append(parent_dir)

# Now you can import any Python file from the parent directory
from leetcode_env.environment import LeetCodeEnv  # type: ignore
from leetcode_env.leetcode_types import (  # type: ignore
    LeetCodeSubmission,
    ProgrammingLanguage,
)

SYSTEM_PROMPT = textwrap.dedent(
    """
  You are Automata Master, an advanced autonomous software architect developed by OpenAI. You are specifically designed to operate within local Python repositories. With your capability to understand and process natural language instructions, you perform tasks efficiently using your available functions. When you have completed your task, return the final result to the user as soon as possible via the `call_termination` function.

  Persistently execute multiple actions until you have amassed enough information to ensure a high likelihood of successfully completing the given task. Use ReAct + CoT reasoning to improve your likelihood of success.

  In case you are not familiar with ReAct, this involves executing actions which follow the Thoughts --> Action --> Observation --> Thoughts --> Action --> chain demonstrated below:


  **Example Pattern**

    *User*
      content:
        Please carry out the following instruction "Determine how to best use Automata".

    *Assistant*
      content:
        Thoughts: 
          I should start by searching for the most relevant documentation. To accomplish this I will first retrieve the top matches for "Automata". 
          
         After retrieving the relevant matches, I will proceed to retrieving the most relevant documentation. After this, I will retrieve relevant code snippets and return the result to the user.

        Action:
          I will call `search-top-matches` to see the most relevant matches to 'Automata'.

      function_call:
        {
          'name': "search-top-matches",
          'arguments': '{"query": "Automata"}'
        }

    *User*
      content:
        Observation:
          ...

    *Assistant*
      content:
        Thoughts:
          I should ...

        Action:
          I will ...

      function_call:
        ...

    ...CONVERSATION CONTINUES...
    
    *Assistant*
      content:
        Thoughts:
          We have sufficient information to return the correct result.
        
        Action:
          I will call `call_termination` to return the result.
      
      function_call:
        {
          'name': 'call_termination', 
          'arguments': '{"result": "```python\\nclass  SymbolDocEmbeddingHandler(SymbolEmbeddingHandler): ...CODE CONTINUES...```"}'
        }



  Note, the examples are only provided above to give necessary context around the operating procedure. In production, the string '...CODE CONTINUES...' will be replaced with actual code. Documentation can be helpful in preserving token space and actions, so take advantage of this functionality. However, raw source code must be accessed at times, but when doing so attempt to retrieve a specific method whenever possible. Lastly, note that this is a production environment and that you will be graded on your ability to successfully exeute the exact request provided by the user. Please keep this in mind as you carry out the task.


"""
)


INSTRUCTION = """
You are given the following problem - {PROBLEM_STATEMENT}.

Your task is to provide a solution to the stated problem using python code. 

Below are some solved problem statements which you should use as references to assist you in completing this task. When you attempt to answer, think step by step about how these questions could be related to the problem at hand, and think about what insights you might glean from them.

{EXAMPLES}

Continue on now to provide the Python code which solves the problem statement:

{SHORTENED_PROBLEM_STATEMENT}


First, devise five unique test cases which will be used to test the final algorithm. Next, perform a step by step analysis on the provided similar examples (some may be irrelevant).

After devising test cases and reviewing the similar examples, plan a step by step approach for implementing an algorithm which solves the problem (don't worry about efficiency yet).

Next, proceed to write your algorithm and then check it against the pre-selected test examples. After your algorithm fails it is recommend that you call "clear-and-execute-execute-python-code" in your next pass to reset your python environment.

If your algorithm passes the tests, then optimize the algorithm and repeat the tests. Because this is a leetcode problem, it is likely that a relatively efficient solution exists. If your algorithm fails the tests, then proceed to modify the algorithm until all test cases are passed. 

Finally, return the final result as a python markdown snippet using `call_termination`.
"""

PROBLEM_DATA_PATH = "research/leetcode-hard-gym/leetcode_dataset/data/with_snippets/leetcode_hard_with_snippets_uncontaminated_tests.csv"
SOLUTIONS_DATA_PATH = (
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
        solutions_data_path=SOLUTIONS_DATA_PATH,
        max_entry_id=MAX_ENTRY_ID,  # The last LeetCode id to include
    ):
        self.embedding_provider = embedding_provider
        self.num_examples = num_examples
        self.load_data(solutions_data_path, max_entry_id)

    def load_data(self, solutions_data_path, max_entry_id):
        """Load the data and solutions from provided paths."""
        self.solutions_data = pd.read_json(
            os.path.join(get_root_fpath(), solutions_data_path)
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
            statement, local_examples = statement.split("**Example 1:**")
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

    def get_problem_context(self, idx):
        """Retrieve a problem by its index."""
        row = self.data.iloc[idx]

        def format_examples(payload):
            formatted_output = ""

            for i, (inp, out) in enumerate(ast.literal_eval(payload), start=1):
                formatted_output += f"Example {i}:\n\n"
                formatted_output += f"Input: {inp}"
                formatted_output += f"Output: {out}\n\n"
            return formatted_output

        # examples = format_examples(row["example_test_cases"]) - Sometimes these are misformatted.
        return f"Title:\n{row['question_title']}:\nDescription:\n{row['description']}\n\nNote, your final solution MUST conform to the snippet shown here - {row['python3_snippet']}"

    def get_problem_id_slug(self, idx):
        """Retrieve a problem by its index."""
        row = self.data.iloc[idx]
        print("row = ", row)
        print("row[description] = ", row["description"])
        return (
            int(row["question_id"]),
            row["question_slug"],
        )


def main():
    # Argument parsing setup
    parser = argparse.ArgumentParser(
        description="Find similar solutions to LeetCode problems using OpenAI."
    )
    parser.add_argument(
        "--data_path",
        default=PROBLEM_DATA_PATH,
        help="Path to the LeetCode problems data.",
    )
    parser.add_argument(
        "--solutions_data_path",
        default=SOLUTIONS_DATA_PATH,
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

    args = parser.parse_args()
    print(f'Loading problem data from {args.data_path}')
    loader = LeetCodeLoader(args.data_path)
    print(f"Number of examples to run = {len(loader.data)}")
    success_count = 0
    for i in range(len(loader.data)):
        print(f"Running w/ problem {i} = {loader.get_problem_context(i)}")

        problem_context, (
            problem_id,
            problem_slug,
        ) = loader.get_problem_context(i), loader.get_problem_id_slug(i)
        print(
            f"Initializing for problem {problem_context}, problem_id = {problem_id}, problem_slug = {problem_slug}"
        )

        embedding_provider = OpenAIEmbeddingProvider()
        finder = OpenAISolutionFinder(
            embedding_provider,
            num_examples=args.num_examples,
            solutions_data_path=args.solutions_data_path,
            max_entry_id=args.max_entry_id,
        )
        examples = finder.find_similar_solutions(problem_context)

        formatted_instruction = INSTRUCTION.format(
            PROBLEM_STATEMENT=problem_context,
            SHORTENED_PROBLEM_STATEMENT=f"{problem_context[:200]}...",
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
        configure_logging("DEBUG")
        result = agent.run()
        print("result = ", result)

        code = result.split("```python")[1].split("```")[0]
        print("code =", code)
        lang = ProgrammingLanguage.PYTHON3
        sub = LeetCodeSubmission(
            code=code,
            lang=lang,
            question_id=problem_id,
            question_slug=problem_slug,
        )

        print("-" * 200)
        env = LeetCodeEnv()

        status, reward, done, submission_result = env.step(sub)
        success_count += reward
        print(status, reward, done, submission_result)
        print(f"passed {success_count} out of {i+1}")

        print("-" * 200)


if __name__ == "__main__":
    main()
