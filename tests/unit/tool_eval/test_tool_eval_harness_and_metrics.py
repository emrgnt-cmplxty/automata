from automata.eval import ToolEvaluationMetrics

from .conftest import EXPECTED_TOOL_ACTIONS, FUNCTION_CALLS, params


def test_tool_evaluation_harness_and_metrics(tool_eval_harness, setup_tool):
    """Test the properties of ToolEvaluationMetrics"""

    (
        mock_openai_toolcompletion_create,
        task_executor,
    ) = setup_tool
    mock_openai_toolcompletion_create.side_effect = params[
        "test_tool_evaluation_harness_and_metrics"
    ]

    expected_actions = [
        [
            EXPECTED_TOOL_ACTIONS[0],
            EXPECTED_TOOL_ACTIONS[1],
        ],
        [
            EXPECTED_TOOL_ACTIONS[0],
            EXPECTED_TOOL_ACTIONS[1],
        ],
    ]

    metrics = tool_eval_harness.evaluate(
        FUNCTION_CALLS, expected_actions, task_executor
    )

    # Assert
    assert isinstance(metrics, ToolEvaluationMetrics)
    assert metrics.total_evaluations == 4
    assert metrics.total_full_matches == 2
    assert metrics.total_partial_matches == 1
    assert metrics.full_match_rate == 0.5
    assert metrics.partial_match_rate == 0.25
