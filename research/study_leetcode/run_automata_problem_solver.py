# sourcery skip: avoid-global-variables, no-relative-imports, require-parameter-annotation, require-return-annotation
# flake8: noqa
"""Study the dataset."""
import argparse
import logging
import os
import random
import sys
from typing import Dict

random.seed(0)

from agentified_solution_oracle import (
    AgentifiedSolutionOracleOpenAIToolkitBuilder,
)
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
from leetcode_env.utils import PySubmissionFormatter


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

    args = parser.parse_args()
    print(f"Loading problem data from {args.problems_data_path}")
    loader = LeetCodeLoader(args.problems_data_path)
    embedding_provider = OpenAIEmbeddingProvider()
    formatter = PySubmissionFormatter
    print(f"Number of examples to run = {len(loader.data)}")
    success_count = 0
    results = {}
    indices = list(range(len(loader.data)))
    random.shuffle(indices)

    for i in indices:
        # try:
        print(f"Running w/ problem {i}:\n\n{loader.get_problem_context(i)}")

        (
            problem_header,
            problem_context,
            (
                problem_id,
                backend_problem_id,
                problem_slug,
            ),
        ) = (
            loader.get_problem_header(i),
            loader.get_problem_context(i),
            loader.get_problem_id_slug(i),
        )
        # print(
        #     f"Initializing for problem {problem_context}, problem_id = {problem_id}, problem_slug = {problem_slug}"
        # )
        print("loader.data[i] = ", loader.data.iloc[i]["example_test_cases"])

        finder = LeetCodeSolutionsFinder(
            embedding_provider,
            max_entry_id=problem_id,
            max_num_examples=args.max_num_examples,
            num_examples_to_screen=args.num_examples_to_screen,
            solutions_data_path=args.solutions_data_path,
            lowest_difficulty=args.lowest_difficulty_supported,
        )

        formatted_instructions = SOLVER_INSTRUCTIONS.format(
            PROBLEM_STATEMENT=problem_context,
            SHORTENED_PROBLEM_STATEMENT=f"{problem_context[:200]}...",
        )

        tools = AgentifiedSolutionOracleOpenAIToolkitBuilder(
            leetcode_solution_finder=finder
        ).build_for_open_ai()

        config = (
            OpenAIAutomataAgentConfigBuilder()
            .with_stream(True)
            .with_verbose(True)
            .with_tools(tools)
            .with_system_template(SOLVER_SYSTEM_PROMPT)
            .build()
        )

        agent = OpenAIAutomataAgent(formatted_instructions, config)

        initial_query = f"{problem_header}"
        extra_context = (
            "Find the best example to help me solve the provided problem."
        )
        # Take the agent's first action before running
        assistant_message = OpenAIChatMessage(
            role="assistant",
            content="Thoughts:\n  I will start by gathering relevant context.\nAction:\n  I will search for similar solutions to the problem",
            function_call=FunctionCall(
                name="solution-oracle",
                arguments={
                    "query": initial_query,
                    "extra_context": extra_context,
                },
            ),
        )
        agent.chat_provider.add_message(assistant_message, agent.session_id)

        solution = finder.find_best_match_and_explanation(
            initial_query, extra_context
        )

        user_message = OpenAIChatMessage(
            role="user",
            content=solution,
        )
        agent.chat_provider.add_message(user_message, agent.session_id)

        configure_logging("DEBUG")
        result = agent.run()

        code = (
            result.split("```python")[1].split("```")[0].replace("\\n", "\n")
        )
        import pdb

        pdb.set_trace()
        break
    #     lang = ProgrammingLanguage.PYTHON3
    #     sub = LeetCodeSubmission(
    #         code=formatter.to_leetcode(code),
    #         lang=lang,
    #         question_id=backend_problem_id,
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


# TODO Rename this here and in `main`
def _log_result(
    result: bool, results: Dict[int, bool], i: int, success_count: int
):
    """Log the result of the current run."""
    results[i] = result
    print("-" * 200)
    print(f"passed {success_count} out of {i+1}")
    print(f"results dict = {results}")
    print("-" * 200)


if __name__ == "__main__":
    main()
