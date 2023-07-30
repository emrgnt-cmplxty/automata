# sourcery skip: no-relative-imports
from automata.eval import ToolEvaluationMetrics

from .conftest import EXPECTED_TOOL_ACTIONS, FUNCTION_CALLS


def test_tool_evaluation_harness_and_metrics(tool_eval_harness, setup_tool):
    """Test the properties of ToolEvaluationMetrics"""

    task_executor = setup_tool

    expected_actions = [
        EXPECTED_TOOL_ACTIONS[0],
        EXPECTED_TOOL_ACTIONS[1],
        EXPECTED_TOOL_ACTIONS[2],
        EXPECTED_TOOL_ACTIONS[3],
        EXPECTED_TOOL_ACTIONS[4],
    ]

    metrics = tool_eval_harness.evaluate(
        FUNCTION_CALLS, expected_actions, task_executor
    )

    # Assert
    assert isinstance(metrics, ToolEvaluationMetrics)
    assert metrics.total_evaluations == 5
    assert metrics.total_full_matches == 2
    assert metrics.total_partial_matches == 4
    assert metrics.full_match_rate == 0.4
    assert metrics.partial_match_rate == 0.8
