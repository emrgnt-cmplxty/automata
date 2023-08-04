# sourcery skip: no-relative-imports
from collections import Counter

from automata.eval import AgentEvaluationMetrics

from .conftest import EXPECTED_CODE_ACTIONS, EXPECTED_FUNCTION_ACTIONS, params


def test_evaluation_harness_and_metrics(agent_eval_harness, tasks, setup):
    """Test the properties of AgentEvaluationMetrics"""

    (
        mock_openai_chatcompletion_create,
        automata_agent,
        task_executor,
    ) = setup
    mock_openai_chatcompletion_create.side_effect = params[
        "test_evaluation_harness_and_metrics"
    ]

    expected_actions = [
        [
            EXPECTED_FUNCTION_ACTIONS[0],
            EXPECTED_FUNCTION_ACTIONS[1],
            EXPECTED_CODE_ACTIONS[0],
            EXPECTED_CODE_ACTIONS[1],
        ],
        [
            EXPECTED_FUNCTION_ACTIONS[0],
            EXPECTED_FUNCTION_ACTIONS[1],
            EXPECTED_CODE_ACTIONS[0],
            EXPECTED_CODE_ACTIONS[1],
        ],
    ]

    metrics = agent_eval_harness.evaluate(
        tasks, expected_actions, task_executor
    )

    # Assert
    assert isinstance(metrics, AgentEvaluationMetrics)
    assert metrics.total_actions == 8
    assert metrics.total_successful_actions == 4
    assert metrics.action_success_rate == 0.5
    assert metrics.total_extra_actions == 2
    assert metrics.full_match_rate == 0.0

    assert metrics.successful_actions_frequency == Counter(
        {
            str(EXPECTED_FUNCTION_ACTIONS[0]): 2,
            str(EXPECTED_CODE_ACTIONS[0]): 2,
        }
    )
    assert metrics.failed_actions_frequency == Counter(
        {
            str(EXPECTED_FUNCTION_ACTIONS[1]): 2,
            str(EXPECTED_CODE_ACTIONS[1]): 2,
        }
    )
    assert metrics.extra_action_frequency == Counter(
        {"call_termination({'result': '```python\\nx = 1```'})": 2}
    )
