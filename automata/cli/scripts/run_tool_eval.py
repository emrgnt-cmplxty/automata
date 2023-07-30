import logging
from typing import List

from automata.cli.cli_utils import initialize_py_module_loader
from automata.eval import (
    SymbolSearchAction,
    SymbolSearchEval,
    SymbolSearchEvalResult,
    ToolEval,
    ToolEvalSetLoader,
    ToolEvaluationHarness,
)
from automata.eval.tool.search_eval import TOP_K_MATCHES
from automata.singletons.dependency_factory import dependency_factory
from automata.tools import ToolExecution
from automata.tools.agent_tool_factory import AgentToolFactory

logger = logging.getLogger(__name__)


def run_eval_harness(
    evals_filepath: str,
    evals: List[ToolEval] = [SymbolSearchEval()],
    *args,
    **kwargs,
) -> None:
    """
    Run evaluation for a list of tasks specified in a JSON file.

    Args:
        evals_filepath (str): Filepath to the JSON file containing evals.

    Returns:
        None
    """

    # Load the tasks and expected actions
    logger.info(f"Loading evals from {evals_filepath}...")

    toolkits = kwargs.get("toolkits")
    if not isinstance(toolkits, str):
        raise ValueError("Toolkits must be a string.")
    tool_dependencies = dependency_factory.build_dependencies_for_tools(
        toolkits.split(",")
    )

    tools = AgentToolFactory.build_tools(
        toolkits.split(","), **tool_dependencies
    )

    eval_loader = ToolEvalSetLoader(evals_filepath)
    tool_execution = ToolExecution(tools)
    evaluation_harness = ToolEvaluationHarness(evals)

    output = evaluation_harness.evaluate(
        eval_loader.function_calls,
        eval_loader.expected_actions,
        tool_execution,
    )
    for result in output.results:
        if isinstance(result, SymbolSearchEvalResult):
            expected_action = result.expected_action
            if not isinstance(expected_action, SymbolSearchAction):
                raise ValueError(
                    "Expected action must be a SymbolSearchAction."
                )
            print(f"Search Query: {expected_action.query}")
            print(f"Truth Top Match: {expected_action.search_results[0]}\n")

            print("- Observed Results - \n")
            if observed_action := result.observed_action:
                if not isinstance(observed_action, SymbolSearchAction):
                    raise ValueError(
                        "Observed action must be a SymbolSearchAction."
                    )

                print(
                    f"Top {TOP_K_MATCHES} Search Results: {observed_action.search_results[:TOP_K_MATCHES]}\n"
                )
                print(
                    f"{TOP_K_MATCHES}-10 Search Results (not used in matching): {observed_action.search_results[TOP_K_MATCHES:]}\n"
                )

            print(
                f"Full Match: {result.is_full_match}\nPartial Match: {result.is_partial_match}"
            )

            print("=" * 150)

    print(output)
    print("=" * 150)


def main(*args, **kwargs) -> None:
    """Main entrypoint for the run_agent_eval script."""

    initialize_py_module_loader(**kwargs)
    run_eval_harness(**kwargs)
