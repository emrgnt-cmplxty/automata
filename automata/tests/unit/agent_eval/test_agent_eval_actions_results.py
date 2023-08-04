# sourcery skip: no-relative-imports
from automata.eval import CodeWritingAction, OpenAIFunctionCallAction
from automata.tasks.task_base import TaskStatus

from .conftest import (
    COMPLICATED_ACTION,
    EXPECTED_CODE_ACTIONS,
    EXPECTED_FUNCTION_ACTIONS,
    mock_openai_response_with_function_completion_message_final,
    params,
)

# TODO - Refactor test eval into multiple tests
# TODO - Include more tests for CodeWriting / FunctionCalling
# which include more exotic types


def test_generate_function_eval_result_match(
    conversation_db,
    tasks,
    function_evaluator,
    setup,
):
    task = tasks[0]
    mock_openai_chatcompletion_create, automata_agent, task_executor = setup
    mock_openai_chatcompletion_create.side_effect = params[
        "test_generate_function_eval_result_match_responses"
    ]
    # Act
    result = function_evaluator.generate_eval_result(
        task, EXPECTED_FUNCTION_ACTIONS, task_executor, run_id="test"
    )

    # Assert
    assert result.is_full_match
    assert result.match_results == {
        action: True for action in EXPECTED_FUNCTION_ACTIONS
    }
    assert result.extra_actions == [
        OpenAIFunctionCallAction(
            name="call_termination", arguments={"result": "Success"}
        )
    ]

    assert task.status == TaskStatus.SUCCESS
    assert task.result == "Observation:\nSuccess\n"

    saved_messages = conversation_db.get_messages(automata_agent.session_id)
    assert len(saved_messages) == 11


def test_generate_eval_result_no_match(
    conversation_db, tasks, function_evaluator, setup
):
    task = tasks[0]
    mock_openai_chatcompletion_create, automata_agent, task_executor = setup
    mock_openai_chatcompletion_create.side_effect = params[
        "test_generate_eval_result_no_match_responses"
    ]

    # Act
    result = function_evaluator.generate_eval_result(
        task, EXPECTED_FUNCTION_ACTIONS, task_executor, run_id="test"
    )

    # Assert
    assert not result.is_full_match
    assert result.match_results == {
        action: False for action in EXPECTED_FUNCTION_ACTIONS
    }
    assert result.extra_actions == [
        OpenAIFunctionCallAction(
            name="function3", arguments={"arg3": "value3"}
        ),
        OpenAIFunctionCallAction(
            name="call_termination", arguments={"result": "Success"}
        ),
    ]


def test_generate_eval_result_partial_match(
    conversation_db, tasks, function_evaluator, setup
):
    task = tasks[0]
    mock_openai_chatcompletion_create, automata_agent, task_executor = setup
    mock_openai_chatcompletion_create.side_effect = params[
        "test_generate_eval_result_partial_match"
    ]

    # Act
    result = function_evaluator.generate_eval_result(
        task, EXPECTED_FUNCTION_ACTIONS, task_executor, run_id="test"
    )

    # Assert
    assert not result.is_full_match
    assert result.match_results == {
        EXPECTED_FUNCTION_ACTIONS[0]: True,
        EXPECTED_FUNCTION_ACTIONS[1]: False,
    }
    assert result.extra_actions == [
        OpenAIFunctionCallAction(
            name="call_termination", arguments={"result": "Success"}
        ),
    ]


def test_generate_code_writing_eval_result_match(
    conversation_db, tasks, code_evaluator, setup
):
    task = tasks[0]
    mock_openai_chatcompletion_create, automata_agent, task_executor = setup
    mock_openai_chatcompletion_create.side_effect = params[
        "test_generate_code_writing_eval_result_match"
    ]
    # Act
    result = code_evaluator.generate_eval_result(
        task, [EXPECTED_CODE_ACTIONS[0]], task_executor, run_id="test"
    )
    # Assert
    assert result.is_full_match
    assert result.match_results == {
        action: True for action in [EXPECTED_CODE_ACTIONS[0]]
    }
    assert result.extra_actions == []


def test_generate_code_writing_eval_result_no_match(
    conversation_db, tasks, code_evaluator, setup
):
    task = tasks[0]
    mock_openai_chatcompletion_create, automata_agent, task_executor = setup
    mock_openai_chatcompletion_create.side_effect = params[
        "test_generate_code_writing_eval_result_no_match"
    ]

    # Act
    result = code_evaluator.generate_eval_result(
        task, EXPECTED_CODE_ACTIONS, task_executor, run_id="test"
    )

    # Assert
    assert not result.is_full_match
    assert result.match_results == {
        action: False for action in EXPECTED_CODE_ACTIONS
    }
    assert result.extra_actions == []


def test_generate_code_writing_eval_result_partial_match(
    conversation_db, tasks, code_evaluator, setup
):
    task = tasks[0]
    mock_openai_chatcompletion_create, automata_agent, task_executor = setup
    mock_openai_chatcompletion_create.side_effect = [
        {
            # TODO - Avoid having multiple call_terminations
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "function_call": {
                            "name": "call_termination",
                            "arguments": '{"result": "```python\nx = 1```"}',
                        },
                        "content": None,
                    }
                }
            ]
        },
        mock_openai_response_with_function_completion_message_final(),
    ]

    # Act
    result = code_evaluator.generate_eval_result(
        task,
        EXPECTED_CODE_ACTIONS,
        task_executor,
        session_id=None,
        run_id="test",
    )

    # Assert
    assert not result.is_full_match
    assert result.match_results == {
        EXPECTED_CODE_ACTIONS[0]: True,
        EXPECTED_CODE_ACTIONS[1]: False,
    }
    assert result.extra_actions == []


def test_composite_eval_result_match(
    conversation_db, tasks, composite_evaluator, setup
):
    task = tasks[0]
    mock_openai_chatcompletion_create, automata_agent, task_executor = setup
    mock_openai_chatcompletion_create.side_effect = params[
        "test_composite_eval_result_match"
    ]

    expected_actions = [
        EXPECTED_FUNCTION_ACTIONS[0],
        EXPECTED_CODE_ACTIONS[0],
        OpenAIFunctionCallAction(
            name="call_termination",
            arguments={"result": "```python\nx = 1```"},
        ),
    ]

    result = composite_evaluator.generate_eval_result(
        task, expected_actions, task_executor, session_id=None, run_id="test"
    )

    assert result.is_full_match
    assert result.match_results == {
        action: True for action in expected_actions
    }
    assert result.extra_actions == []


def test_composite_eval_no_match(
    conversation_db, tasks, composite_evaluator, setup
):
    task = tasks[0]

    mock_openai_chatcompletion_create, automata_agent, task_executor = setup
    mock_openai_chatcompletion_create.side_effect = params[
        "test_composite_eval_no_match"
    ]

    expected_actions = [
        EXPECTED_FUNCTION_ACTIONS[0],
        EXPECTED_CODE_ACTIONS[0],
    ]

    result = composite_evaluator.generate_eval_result(
        task, expected_actions, task_executor, session_id=None, run_id="test"
    )

    assert result.is_full_match is False
    assert result.match_results == {
        EXPECTED_FUNCTION_ACTIONS[0]: False,
        EXPECTED_CODE_ACTIONS[0]: False,
    }
    assert result.extra_actions == [
        OpenAIFunctionCallAction(
            name="call_termination", arguments={"result": "Success"}
        )
    ]


def test_code_execution_error(composite_evaluator, tasks, setup):
    task = tasks[0]

    mock_openai_chatcompletion_create, automata_agent, task_executor = setup
    mock_openai_chatcompletion_create.side_effect = params[
        "test_composite_eval_no_match"
    ]

    expected_actions = [
        EXPECTED_FUNCTION_ACTIONS[0],
        EXPECTED_CODE_ACTIONS[0],
    ]

    result = composite_evaluator.generate_eval_result(
        task, expected_actions, task_executor, session_id=None, run_id="test"
    )

    assert result.is_full_match is False
    assert result.match_results == {
        EXPECTED_FUNCTION_ACTIONS[0]: False,
        EXPECTED_CODE_ACTIONS[0]: False,
    }
    assert result.extra_actions == [
        OpenAIFunctionCallAction(
            name="call_termination", arguments={"result": "Success"}
        )
    ]


def test_matching():
    obj1 = CodeWritingAction(py_object=1, error=None)
    obj2 = CodeWritingAction(py_object=2.0, error=None)
    obj3 = CodeWritingAction(py_object=1, error=None)

    action_1 = CodeWritingAction(py_object=obj1, error=None)
    action_2 = CodeWritingAction(py_object=obj2, error=None)
    action_3 = CodeWritingAction(py_object=obj3, error=None)

    assert action_1 != action_2
    assert action_1 == action_3


def test_complex_payload():
    payload_0 = EXPECTED_CODE_ACTIONS[0].to_payload()
    loaded_action_0 = CodeWritingAction.from_payload(payload_0)
    assert EXPECTED_CODE_ACTIONS[0] == loaded_action_0

    payload_1 = EXPECTED_CODE_ACTIONS[1].to_payload()
    loaded_action_1 = CodeWritingAction.from_payload(payload_1)
    assert EXPECTED_CODE_ACTIONS[1] == loaded_action_1

    payload_2 = COMPLICATED_ACTION.to_payload()
    loaded_action_2 = CodeWritingAction.from_payload(payload_2)
    assert COMPLICATED_ACTION == loaded_action_2
