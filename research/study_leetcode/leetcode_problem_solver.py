# sourcery skip: docstrings-for-classes, docstrings-for-functions, docstrings-for-modules, require-parameter-annotation, require-return-annotation
import random
import textwrap
from typing import Optional

from agentified_solution_oracle import (
    AgentifiedSolutionOracleOpenAIToolkitBuilder,
)
from constants import (
    EVAL_SYSTEM_PROMPT,
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
from automata.config import (
    OpenAIAutomataAgentConfig,
    OpenAIAutomataAgentConfigBuilder,
)
from automata.llm import (
    FunctionCall,
    OpenAIChatMessage,
    OpenAIEmbeddingProvider,
)
from automata.tools.agent_tool_factory import AgentToolFactory


class LeetCodeSolver:
    def __init__(self, num_examples: int = 0):
        # sourcery skip: docstrings-for-functions
        self.results = {}
        self.count, self.success_count = 0, 0
        self.indices = list(range(num_examples))
        random.seed(0)
        random.shuffle(self.indices)

    def _get_agent_config(
        self, system_prompt: str, solutions_finder: LeetCodeSolutionsFinder
    ) -> OpenAIAutomataAgentConfig:
        tools = AgentifiedSolutionOracleOpenAIToolkitBuilder(
            leetcode_solution_finder=solutions_finder
        ).build_for_open_ai()  # type: ignore

        return (
            OpenAIAutomataAgentConfigBuilder()
            .with_stream(True)
            .with_verbose(True)
            .with_tools(tools)  # type: ignore
            .with_system_template(system_prompt)
            .build()
        )

    def construct_agent(
        self,
        problem_header: str,
        formatted_instructions: str,
        solutions_finder: LeetCodeSolutionsFinder,
        include_leetcode_best_old_solution: bool = True,
    ) -> OpenAIAutomataAgent:
        """Construct an agent to solve the given problem."""

        config = self._get_agent_config(SOLVER_SYSTEM_PROMPT, solutions_finder)
        agent = OpenAIAutomataAgent(formatted_instructions, config)

        if include_leetcode_best_old_solution:
            self.add_best_related_leetcode_solution(
                problem_header, agent, solutions_finder
            )
        return agent

    @staticmethod
    def add_best_related_leetcode_solution(
        problem_header, agent, solutions_finder
    ):
        """
        Add messages to the agent which correspond to finding a related solution.

        The information is injected in accordance with the expected conversation
        format.
        """
        initial_query = f"{problem_header}"
        extra_context = (
            "Find the best example to help me solve the provided problem."
        )
        assistant_message = OpenAIChatMessage(
            role="assistant",
            content="Thoughts:\n  I will start by gathering relevant context.\nAction:\n  I will search for similar solutions to the stated problem.",
            function_call=FunctionCall(
                name="solution-oracle",
                arguments={
                    "query": initial_query,
                    "extra_context": extra_context,
                },
            ),
        )
        agent.chat_provider.add_message(assistant_message, agent.session_id)

        solution = solutions_finder.find_best_match_and_explanation(
            initial_query, extra_context
        )

        user_message = OpenAIChatMessage(
            role="user",
            content=solution,
        )
        agent.chat_provider.add_message(user_message, agent.session_id)

    def build_reflection_agent(
        self,
        problem_statement: str,
        attempted_solution: str,
        test_results: Optional[str],
        exception: Optional[str],
        solutions_finder: LeetCodeSolutionsFinder,
    ) -> OpenAIAutomataAgent:
        """Builds an agent which returns a reflection when executed"""
        config = self._get_agent_config(EVAL_SYSTEM_PROMPT, solutions_finder)

        """Builds the reflection agent"""
        formatted_reflexion_instruction = textwrap.dedent(
            f"""
        Problem:
        {problem_statement}

        Attempted Solution:
        {attempted_solution}

        Test Result:
        {test_results}


        Test Exception:
        {exception}

        Please follow these steps in your analysis:

        1. Identify the failed test cases and explain what the expected and actual results were.
        2. Analyze the specific parts of the code that might have led to these failed test cases.
        3. Provide a concise explanation of the nature of the errors without correcting the code or explaining the entire algorithm.

        Do not include the corrected code or a detailed explanation of the entire algorithm. Focus solely on the parts that have gone wrong.
        
        Include all of your analysis in the result returned with `call_termination`.
        """
        )

        return OpenAIAutomataAgent(formatted_reflexion_instruction, config)

    def log_result(self, index: int, result: bool):
        """Log the result of the current run."""
        self.results[index] = result
        self.count += 1
        if result:
            self.success_count += 1
        print("-" * 200)
        print(f"passed {self.success_count} out of {self.count}")
        print(f"results dict = {self.results}")
        print("-" * 200)
