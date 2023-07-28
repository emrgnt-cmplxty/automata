# sourcery skip: no-relative-imports
from automata.agent.openai_agent import OpenAIChatMessage
from automata.eval.agent.agent_eval import AgentEvalResult
from automata.tasks.task_base import TaskStatus

from .conftest import EXPECTED_CODE_ACTIONS, EXPECTED_FUNCTION_ACTIONS, params


# Standalone test for the AgentEvalResultDatabase
def test_eval_result_writer(eval_db):
    # Generate a test EvalResult
    action1 = EXPECTED_CODE_ACTIONS[0]
    action2 = EXPECTED_CODE_ACTIONS[1]
    eval_result = AgentEvalResult(
        match_results={action1: True, action2: False},
        extra_actions=[action2],
        session_id="test_session",
    )

    # Write the result to the database
    eval_db.write_result(eval_result)

    # Retrieve the result from the database
    retrieved_results = eval_db.get_results("test_session")

    # Check that the retrieved result matches the original result
    assert len(retrieved_results) == 1
    retrieved_result = retrieved_results[0]
    assert retrieved_result.is_full_match == eval_result.is_full_match
    assert retrieved_result.match_results == eval_result.match_results
    assert retrieved_result.extra_actions == eval_result.extra_actions
    assert retrieved_result.session_id == eval_result.session_id


def test_task_evaluation_with_database_integration(
    matched_setup,
    composite_evaluator,
    conversation_db,
    task_w_agent_matched_session,
):
    (
        mock_openai_chatcompletion_create,
        automata_agent,
        task_executor,
        task_registry,
    ) = matched_setup

    mock_conversation = params["test_composite_eval_partial_match"]
    mock_openai_chatcompletion_create.side_effect = mock_conversation

    expected_actions = [
        EXPECTED_FUNCTION_ACTIONS[0],
        EXPECTED_CODE_ACTIONS[0],
    ]

    composite_evaluator.generate_eval_result(
        task_w_agent_matched_session,
        expected_actions,
        task_executor,
        run_id="test",
    )

    session_id = str(task_w_agent_matched_session.session_id)
    fetched_task = task_registry.fetch_task_by_id(session_id)
    fetched_conversation = conversation_db.get_messages(session_id)

    assert fetched_task.status == TaskStatus.SUCCESS
    assert fetched_task.session_id == automata_agent.session_id

    mock_msg_0 = OpenAIChatMessage(
        **mock_conversation[0]["choices"][0]["message"]
    )
    assert fetched_conversation[-4].role == mock_msg_0.role
    assert fetched_conversation[-4].content == mock_msg_0.content
    # TODO - We need proper loading of the function_call object
    # assert fetched_conversation[0].function_call == mock_msg_0.function_call

    mock_msg_1 = OpenAIChatMessage(
        **mock_conversation[1]["choices"][0]["message"]
    )
    # TODO - We skip the user feedback message, should probably check that
    assert fetched_conversation[-2].role == mock_msg_1.role
    assert fetched_conversation[-2].content == mock_msg_1.content
