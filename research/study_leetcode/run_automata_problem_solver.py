# sourcery skip: avoid-global-variables, no-relative-imports, require-parameter-annotation, require-return-annotation
# flake8: noqa
"""Study the dataset."""
import argparse
import logging
import os
import sys
from copy import deepcopy
from typing import Dict

from constants import (
    LEETCODE_PROBLEMS_PATH,
    LEETCODE_SOLUTIONS_PATH,
    LOWEST_DIFFICULTY_SUPPORTED,
    MAX_CONTEXT_EXAMPLES,
    MAX_NUM_EXAMPLES_TO_SCREEN,
    SOLVER_INSTRUCTIONS,
    SOLVER_SYSTEM_PROMPT,
)
from leetcode_problem_solver import LeetCodeSolver
from leetcode_problems_loader import LeetCodeLoader
from leetcode_solutions_finder import LeetCodeSolutionsFinder
from leetcode_test_stand import LeetCodeTestStand

from automata.core.utils import get_root_fpath
from automata.llm import (
    FunctionCall,
    OpenAIChatMessage,
    OpenAIEmbeddingProvider,
)
from automata.singletons.dependency_factory import dependency_factory
from automata.tools.agent_tool_factory import AgentToolFactory

logger = logging.getLogger(__name__)

# Get the absolute path of the parent directory
leetcode_gym_location = os.path.join(
    get_root_fpath(), "research", "leetcode_hard_gym"  # , "leetcode_env"
)

# Add the parent directory to the PYTHONPATH
sys.path.append(leetcode_gym_location)

# Now we can import any Python file from the parent directory
from leetcode_env.environment import LeetCodeEnv  # type: ignore
from leetcode_env.leetcode_types import (  # type: ignore
    LeetCodeSubmission,
    ProgrammingLanguage,
)

NUM_REFLECTIONS = 5


def main():  # sourcery skip: docstrings-for-functions
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
    parser.add_argument(
        "--include_leetcode_best_old_solution",
        type=str,
        default=True,
        help="Should related solutions be returned to the agent?",
    )

    args = parser.parse_args()
    print(f"Loading problem data from {args.problems_data_path}")
    loader = LeetCodeLoader(args.problems_data_path)
    num_examples = len(loader.data)
    print(f"Number of examples to run = {num_examples}")

    solver = LeetCodeSolver(num_examples)
    embedding_provider = OpenAIEmbeddingProvider()
    test_stand = LeetCodeTestStand(loader=loader)

    for index in solver.indices:
        try:
            problem_context = loader.get_problem_context(index)
            agent_message_buffer = []

            print(
                f"Running w/ problem at index {index} and context:\n\n{problem_context}"
            )

            solutions_finder = LeetCodeSolutionsFinder(
                embedding_provider,
                max_entry_id=loader.get_frontend_problem_id(
                    index
                ),  # Solutions are indexed along frontend problem id
                max_num_examples=args.max_num_examples,
                num_examples_to_screen=args.num_examples_to_screen,
                solutions_data_path=args.solutions_data_path,
                lowest_difficulty=args.lowest_difficulty_supported,
            )

            print(
                f"Running w/ problem at index {index} and context:\n\n{problem_context}"
            )

            # Construcs an agent that will provide a solution to the
            # given LeetCode problem when ran

            solution_agent = solver.construct_agent(
                loader.get_problem_header(index),
                formatted_instructions,
                solutions_finder,
                args.include_leetcode_best_old_solution,
            )

            # If a related solution was fetched, update the agent message buffer
            # so that these messages will be included after reflexion in future iterations
            if args.include_leetcode_best_old_solution:
                agent_message_buffer = deepcopy(
                    solution_agent.conversation.messages[-2:]
                )
                print(
                    f"Storing an agent message buffer = {agent_message_buffer}"
                )
            result = solution_agent.run()

            cleaned_result = (
                result.split("```python")[1]
                .split("```")[0]
                .replace("\\n", "\n")
            )
            print(f"Final Cleaned Result:\n{cleaned_result}")

            exception, test_results = test_stand.run_tests_for_example(
                index, cleaned_result
            )

            for i in range(NUM_REFLECTIONS):
                reflection_agent = solver.build_reflection_agent(
                    loader.get_problem_header(index).split("Constraints")[0],
                    result,
                    test_results,
                    exception,
                    solutions_finder,
                )

                reflection = reflection_agent.run()

                solution_agent = solver.construct_agent(
                    loader.get_problem_header(index),
                    formatted_instructions,
                    solutions_finder,
                    False,
                )

                solution_agent.conversation.messages.extend(
                    agent_message_buffer
                )

                query_message = OpenAIChatMessage(
                    role="assistant",
                    content="Thoughts:\n  Excellent, the previous solution will be helpful in guiding our best solution. Further, we should query the solution history for additional information, this is a query we can only do once.\nAction:\n  I will now query the past solution history.",
                    function_call=FunctionCall(
                        name="attempted-solution-history",
                        arguments={
                            "query": "Past solutions for 'Minimum Reverse Operations'"
                        },
                    ),
                )

                solution_agent.conversation.messages.append(query_message)

                response_message = OpenAIChatMessage(
                    role="user",
                    content=f"Previous Result:\n{result}\n\nTest Results:\n{test_results}\n\nExceptions:\n{exception}\n\nReflections:\n{reflection}",
                )

                solution_agent.conversation.messages.append(response_message)

                result = solution_agent.run()

                cleaned_result = (
                    result.split("```python")[1]
                    .split("```")[0]
                    .replace("\\n", "\n")
                )
                print(f"Final Cleaned Result:\n{cleaned_result}")

                exception, test_results = test_stand.run_tests_for_example(
                    index, cleaned_result
                )

            print(
                f"~~~Testing~~~\n\nException:\n{exception}\nTest Result:\n{test_results}"
            )

            def prep_for_leetcode(code: str) -> str:
                lines = code.split("\n")
                modified_lines = ["class Solution():"]
                for line in lines:
                    if line.startswith("def "):
                        line = "def " + line[4:].replace("(", "(self, ", 1)
                    modified_lines.append(f"  {line}")
                return "\n".join(modified_lines)

            lang = ProgrammingLanguage.PYTHON3
            sub = LeetCodeSubmission(
                code=prep_for_leetcode(cleaned_result),
                lang=lang,
                question_id=loader.get_backend_problem_id(index),
                question_slug=loader.get_problem_slug(index),
            )

            exception, test_results = test_stand.run_tests_for_example(
                index, cleaned_result
            )

            status, reward, done, submission_result = env.step(sub)
            print(status, reward, done, submission_result)
            solver.log_result(index, reward)
        except:
            print("Failed to run example")
            solver.log_result(index, False)


if __name__ == "__main__":
    from automata.cli.commands import configure_logging

    configure_logging("DEBUG")
    main()
