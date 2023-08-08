# sourcery skip: avoid-global-variables, no-relative-imports, require-parameter-annotation, require-return-annotation
# flake8: noqa
"""Study the dataset."""
import argparse
import ast
import logging
import os
import sys

import pandas as pd
from constants import (
    LEETCODE_PROBLEMS_PATH,
    LEETCODE_SOLUTIONS_PATH,
    LOWEST_DIFFICULTY_SUPPORTED,
    MAX_CONTEXT_EXAMPLES,
    MAX_NUM_EXAMPLES_TO_SCREEN,
    SOLVER_INSTRUCTIONS,
    SOLVER_SYSTEM_PROMPT,
)
from leetcode_problems_loader import LeetCodeLoader
from leetcode_solutions_finder import LeetCodeSolutionsFinder

from automata.agent import OpenAIAutomataAgent
from automata.cli.commands import configure_logging
from automata.config import OpenAIAutomataAgentConfigBuilder
from automata.core.utils import get_root_fpath
from automata.llm import OpenAIEmbeddingProvider
from automata.singletons.dependency_factory import dependency_factory
from automata.tools.agent_tool_factory import AgentToolFactory

logger = logging.getLogger(__name__)

# Get the absolute path of the parent directory
leetcode_gym_location = os.path.join(
    get_root_fpath(), "research", "leetcode-hard-gym"  # , "leetcode_env"
)

# Add the parent directory to the PYTHONPATH
sys.path.append(leetcode_gym_location)

# Now we can import any Python file from the parent directory
from leetcode_env.environment import LeetCodeEnv  # type: ignore
from leetcode_env.leetcode_types import (  # type: ignore
    LeetCodeSubmission,
    ProgrammingLanguage,
)


def main():
    # Argument parsing setup
    parser = argparse.ArgumentParser(
        description="Find similar solutions to LeetCode problems using OpenAI."
    )
    parser.add_argument(
        "--problems_data_path",
        default=LEETCODE_PROBLEMS_PATH,
        help="Path to the LeetCode problems data.",
    )
    parser.add_argument(
        "--solutions_data_path",
        default=LEETCODE_SOLUTIONS_PATH,
        help="Path to the solutions JSON file.",
    )
    parser.add_argument(
        "--max_num_examples",
        type=int,
        default=MAX_CONTEXT_EXAMPLES,
        help="Number of example solutions to display.",
    )
    parser.add_argument(
        "--num_examples_to_screen",
        type=int,
        default=MAX_NUM_EXAMPLES_TO_SCREEN,
        help="Number of example solutions to display.",
    )
    parser.add_argument(
        "--lowest_difficulty_supported",
        type=str,
        default=LOWEST_DIFFICULTY_SUPPORTED,
        help="Lowest difficulty to support for solutions searched over.",
    )

    args = parser.parse_args()
    print(f"Loading problem data from {args.problems_data_path}")
    loader = LeetCodeLoader(args.problems_data_path)
    embedding_provider = OpenAIEmbeddingProvider()

    print(f"Number of examples to run = {len(loader.data)}")
    success_count = 0
    results = {}
    for i in range(len(loader.data)):
        # try:
        print(f"Running w/ problem {i}:\n\n{loader.get_problem_context(i)}")

        (
            problem_header,
            problem_context,
            (
                problem_id,
                problem_slug,
            ),
        ) = (
            loader.get_problem_header(i),
            loader.get_problem_context(i),
            loader.get_problem_id_slug(i),
        )
        print(
            f"Initializing for problem {problem_context}, problem_id = {problem_id}, problem_slug = {problem_slug}"
        )

        finder = LeetCodeSolutionsFinder(
            embedding_provider,
            max_entry_id=problem_id,
            max_num_examples=args.max_num_examples,
            num_examples_to_screen=args.num_examples_to_screen,
            solutions_data_path=args.solutions_data_path,
            lowest_difficulty=args.lowest_difficulty_supported,
        )

        examples = finder.find_best_solution_and_explanation(problem_header)
        break

    #     formatted_instructions = SOLVER_INSTRUCTIONS.format(
    #         PROBLEM_STATEMENT=problem_context,
    #         SHORTENED_PROBLEM_STATEMENT=f"{problem_context[:200]}...",
    #         EXAMPLES=examples,
    #     )

    #     toolkits = ["py-interpreter"]
    #     tool_dependencies = (
    #         dependency_factory.build_dependencies_for_tools(toolkits)
    #     )
    #     tools = AgentToolFactory.build_tools(toolkits, **tool_dependencies)

    #     config = (
    #         OpenAIAutomataAgentConfigBuilder()
    #         .with_stream(True)
    #         .with_verbose(True)
    #         .with_tools(tools)
    #         .with_system_template(SOLVER_SYSTEM_PROMPT)
    #         .build()
    #     )

    #     agent = OpenAIAutomataAgent(formatted_instructions, config)
    #     configure_logging("DEBUG")
    #     result = agent.run()

    #     code = result.split("```python")[1].split("```")[0]
    #     lang = ProgrammingLanguage.PYTHON3
    #     sub = LeetCodeSubmission(
    #         code=code,
    #         lang=lang,
    #         question_id=problem_id,
    #         question_slug=problem_slug,
    #     )

    #     env = LeetCodeEnv()

    #     status, reward, done, submission_result = env.step(sub)
    #     success_count += reward
    #     print(status, reward, done, submission_result)
    #     _log_result(reward, results, i, success_count)
    # except Exception as e:
    #     print(f"Exception occurred = {e}")
    #     _log_result(False, results, i, success_count)
    # break


# TODO Rename this here and in `main`
def _log_result(result, results, i, success_count):
    results[i] = result
    print("-" * 200)
    print(f"passed {success_count} out of {i+1}")
    print(f"results dict = {results}")
    print("-" * 200)


if __name__ == "__main__":
    main()
