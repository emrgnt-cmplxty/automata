import os
from collections import Counter
from unittest.mock import MagicMock

import pytest

from automata.agent.providers import OpenAIChatMessage
from automata.eval import (
    CodeWritingAction,
    CodeWritingEval,
    CompositeEval,
    EvalResult,
    EvalResultDatabase,
    EvaluationHarness,
    EvaluationMetrics,
    OpenAIFunctionCallAction,
    OpenAIFunctionEval,
)
from automata.memory_store import OpenAIAutomataConversationDatabase
from automata.tasks.base import TaskStatus
from automata.tasks.executor import (
    AutomataTaskExecutor,
    IAutomataTaskExecution,
)
from automata.tasks.registry import AutomataTaskRegistry
from automata.tasks.task_database import AutomataAgentTaskDatabase

# TODO - Refactor test eval into multiple tests
# TODO - Include more tests for CodeWriting / FunctionCalling
# which include more exotic types


@pytest.fixture
def evaluator():
    return OpenAIFunctionEval()


@pytest.fixture
def code_evaluator():
    return CodeWritingEval(target_variables=["x", "y", "z"])


@pytest.fixture
def composite_evaluator(evaluator, code_evaluator):
    evaluators = [evaluator, code_evaluator]
    return CompositeEval(evaluators)


@pytest.fixture
def eval_harness(evaluator, code_evaluator):
    return EvaluationHarness([evaluator, code_evaluator])


@pytest.fixture(scope="module", autouse=True)
def conversation_db(tmpdir_factory):
    db_file = tmpdir_factory.mktemp("data").join("test.db")
    db = OpenAIAutomataConversationDatabase(str(db_file))
    yield db
    db.close()
    if os.path.exists(str(db_file)):
        os.remove(str(db_file))


def mock_openai_response_with_function_completion_message_1():
    return {
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "function_call": {
                        "name": "function1",
                        "arguments": '{"arg1": "value1"}',
                    },
                    "content": None,
                }
            }
        ]
    }


def mock_openai_response_with_function_completion_message_2():
    return {
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "function_call": {
                        "name": "function2",
                        "arguments": '{"arg2": "value2"}',
                    },
                    "content": None,
                }
            }
        ]
    }


def mock_openai_response_with_function_completion_message_final():
    return {
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "function_call": {
                        "name": "call_termination",
                        "arguments": '{"result": "Success"}',
                    },
                    "content": None,
                }
            }
        ]
    }


def mock_openai_response_with_function_completion_message_3():
    return {
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "function_call": {
                        "name": "function3",
                        "arguments": '{"arg3": "value3"}',
                    },
                    "content": None,
                }
            }
        ]
    }


def mock_openai_response_with_code_action_completion_message_x():
    return {
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": "```python\nx = 1```",
                }
            }
        ]
    }


def mock_openai_response_with_code_action_completion_message_y():
    return {
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": "```python\ny = 'test'```",
                }
            }
        ]
    }


def mock_openai_response_with_code_action_completion_message_z():
    return {
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": "```python\nz = 3.14```",
                }
            }
        ]
    }


def mock_openai_response_with_bad_code_action_completion_message_z():
    return {
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": "```python\nz = 3.1.4```",
                }
            }
        ]
    }


EXPECTED_FUNCTION_ACTIONS = [
    OpenAIFunctionCallAction(name="function1", arguments={"arg1": "value1"}),
    OpenAIFunctionCallAction(name="function2", arguments={"arg2": "value2"}),
]


EXPECTED_CODE_ACTIONS = [
    CodeWritingAction(object_types="int", object_value_repr="1"),
    CodeWritingAction(object_types="str", object_value_repr="test"),
]


@pytest.fixture
def setup(
    mocker, automata_agent, task, task2, environment, registry, conversation_db
):
    # Mock the API response
    mock_openai_chatcompletion_create = mocker.patch(
        "openai.ChatCompletion.create"
    )

    # Register and setup task
    registry.register(task)
    environment.setup(task)

    registry.register(task2)
    environment.setup(task2)

    # Use the agent's set_database_provider method
    automata_agent.set_database_provider(conversation_db)

    execution = IAutomataTaskExecution()
    IAutomataTaskExecution._build_agent = MagicMock(
        return_value=automata_agent
    )
    task_executor = AutomataTaskExecutor(execution)

    return mock_openai_chatcompletion_create, automata_agent, task_executor


# TODO - Cleanup these fixtures and reduce copy pasta


@pytest.fixture(scope="module", autouse=True)
def task_db(tmpdir_factory):
    db_file = tmpdir_factory.mktemp("data").join("test_task.db")
    db = AutomataAgentTaskDatabase(str(db_file))
    yield db
    db.close()
    if os.path.exists(str(db_file)):
        os.remove(str(db_file))


@pytest.fixture(scope="module", autouse=True)
def eval_db(tmpdir_factory):
    db_file = tmpdir_factory.mktemp("data").join("test_eval.db")
    db = EvalResultDatabase(str(db_file))
    yield db
    db.close()
    if os.path.exists(str(db_file)):
        os.remove(str(db_file))


@pytest.fixture
def real_registry(task_db):
    return AutomataTaskRegistry(task_db)


@pytest.fixture
def setup_real(
    mocker,
    automata_agent,
    task_w_agent_session,
    environment,
    real_registry,
    conversation_db,
):
    # Mock the API response
    mock_openai_chatcompletion_create = mocker.patch(
        "openai.ChatCompletion.create"
    )

    # Register and setup task
    real_registry.register(task_w_agent_session)
    environment.setup(task_w_agent_session)

    # Use the agent's set_database_provider method
    automata_agent.set_database_provider(conversation_db)

    execution = IAutomataTaskExecution()
    IAutomataTaskExecution._build_agent = MagicMock(
        return_value=automata_agent
    )
    task_executor = AutomataTaskExecutor(execution)

    return (
        mock_openai_chatcompletion_create,
        automata_agent,
        task_executor,
        real_registry,
    )


params = {
    "test_generate_function_eval_result_match_responses": [
        mock_openai_response_with_function_completion_message_1(),
        mock_openai_response_with_function_completion_message_2(),
        mock_openai_response_with_function_completion_message_final(),
    ],
    "test_generate_eval_result_no_match_responses": [
        mock_openai_response_with_function_completion_message_3(),
        mock_openai_response_with_function_completion_message_final(),
    ],
    "test_generate_eval_result_partial_match": [
        mock_openai_response_with_function_completion_message_1(),
        mock_openai_response_with_function_completion_message_final(),
    ],
    "test_generate_code_writing_eval_result_match": [
        mock_openai_response_with_code_action_completion_message_x(),
        mock_openai_response_with_code_action_completion_message_y(),
        mock_openai_response_with_code_action_completion_message_z(),
        mock_openai_response_with_function_completion_message_final(),
    ],
    "test_generate_code_writing_eval_result_partial_match": [
        mock_openai_response_with_code_action_completion_message_x(),
        mock_openai_response_with_function_completion_message_final(),
    ],
    "test_generate_code_writing_eval_result_no_match": [
        mock_openai_response_with_function_completion_message_final(),
    ],
    "test_composite_eval_result_match": [
        mock_openai_response_with_function_completion_message_1(),
        mock_openai_response_with_code_action_completion_message_x(),
        mock_openai_response_with_code_action_completion_message_z(),
        mock_openai_response_with_function_completion_message_final(),
    ],
    "test_composite_eval_partial_match": [
        mock_openai_response_with_function_completion_message_1(),
        mock_openai_response_with_function_completion_message_final(),
    ],
    "test_composite_eval_no_match": [
        mock_openai_response_with_function_completion_message_final(),
    ],
    "test_evaluation_harness_and_metrics": [
        mock_openai_response_with_function_completion_message_1(),
        mock_openai_response_with_code_action_completion_message_x(),
        mock_openai_response_with_function_completion_message_final(),
    ],
    "test_bad_code_action_completion": [
        mock_openai_response_with_bad_code_action_completion_message_z(),
    ],
}


def test_generate_function_eval_result_match(
    conversation_db, task, evaluator, setup
):
    mock_openai_chatcompletion_create, automata_agent, task_executor = setup
    mock_openai_chatcompletion_create.side_effect = params[
        "test_generate_function_eval_result_match_responses"
    ]
    # Act
    result = evaluator.generate_eval_result(
        task, EXPECTED_FUNCTION_ACTIONS, task_executor
    )

    # Assert
    assert result.full_match
    assert result.match_result == {
        action: True for action in EXPECTED_FUNCTION_ACTIONS
    }
    assert result.extra_actions == [
        OpenAIFunctionCallAction(
            name="call_termination", arguments={"result": "Success"}
        )
    ]

    assert task.status == TaskStatus.SUCCESS
    assert task.result == "Success"

    saved_messages = conversation_db.get_messages(automata_agent.session_id)
    assert len(saved_messages) == 11


def test_generate_eval_result_no_match(
    conversation_db, task, evaluator, setup
):
    mock_openai_chatcompletion_create, automata_agent, task_executor = setup
    mock_openai_chatcompletion_create.side_effect = params[
        "test_generate_eval_result_no_match_responses"
    ]

    # Act
    result = evaluator.generate_eval_result(
        task, EXPECTED_FUNCTION_ACTIONS, task_executor
    )

    # Assert
    assert not result.full_match
    assert result.match_result == {
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
    conversation_db, task, evaluator, setup
):
    mock_openai_chatcompletion_create, automata_agent, task_executor = setup
    mock_openai_chatcompletion_create.side_effect = params[
        "test_generate_eval_result_partial_match"
    ]

    # Act
    result = evaluator.generate_eval_result(
        task, EXPECTED_FUNCTION_ACTIONS, task_executor
    )

    # Assert
    assert not result.full_match
    assert result.match_result == {
        EXPECTED_FUNCTION_ACTIONS[0]: True,
        EXPECTED_FUNCTION_ACTIONS[1]: False,
    }
    assert result.extra_actions == [
        OpenAIFunctionCallAction(
            name="call_termination", arguments={"result": "Success"}
        ),
    ]


def test_generate_code_writing_eval_result_match(
    conversation_db, task, code_evaluator, setup
):
    mock_openai_chatcompletion_create, automata_agent, task_executor = setup
    mock_openai_chatcompletion_create.side_effect = params[
        "test_generate_code_writing_eval_result_match"
    ]

    # Act
    result = code_evaluator.generate_eval_result(
        task, EXPECTED_CODE_ACTIONS, task_executor
    )

    # Assert
    assert result.full_match
    assert result.match_result == {
        action: True for action in EXPECTED_CODE_ACTIONS
    }
    assert result.extra_actions == [
        CodeWritingAction(object_value_repr="3.14", object_types="float")
    ]


def test_generate_code_writing_eval_result_no_match(
    conversation_db, task, code_evaluator, setup
):
    mock_openai_chatcompletion_create, automata_agent, task_executor = setup
    mock_openai_chatcompletion_create.side_effect = params[
        "test_generate_code_writing_eval_result_no_match"
    ]

    # Act
    result = code_evaluator.generate_eval_result(
        task, EXPECTED_CODE_ACTIONS, task_executor
    )

    # Assert
    assert not result.full_match
    assert result.match_result == {
        action: False for action in EXPECTED_CODE_ACTIONS
    }
    assert result.extra_actions == []


def test_generate_code_writing_eval_result_partial_match(
    conversation_db, task, code_evaluator, setup
):
    mock_openai_chatcompletion_create, automata_agent, task_executor = setup
    mock_openai_chatcompletion_create.side_effect = [
        {
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": "```python\nx = 1```",
                    }
                }
            ]
        },
        mock_openai_response_with_function_completion_message_final(),
    ]

    # Act
    result = code_evaluator.generate_eval_result(
        task, EXPECTED_CODE_ACTIONS, task_executor
    )

    # Assert
    assert not result.full_match
    assert result.match_result == {
        EXPECTED_CODE_ACTIONS[0]: True,
        EXPECTED_CODE_ACTIONS[1]: False,
    }
    assert result.extra_actions == []


def test_composite_eval_result_match(
    conversation_db, task, composite_evaluator, setup
):
    mock_openai_chatcompletion_create, automata_agent, task_executor = setup
    mock_openai_chatcompletion_create.side_effect = params[
        "test_composite_eval_result_match"
    ]

    expected_actions = [
        EXPECTED_FUNCTION_ACTIONS[0],
        EXPECTED_CODE_ACTIONS[0],
        OpenAIFunctionCallAction(
            name="call_termination", arguments={"result": "Success"}
        ),
    ]

    result = composite_evaluator.generate_eval_result(
        task, expected_actions, task_executor
    )

    assert result.full_match
    assert result.match_result == {action: True for action in expected_actions}
    assert result.extra_actions == [
        CodeWritingAction(object_value_repr="3.14", object_types="float"),
    ]


def test_composite_eval_no_match(
    conversation_db, task, composite_evaluator, setup
):
    mock_openai_chatcompletion_create, automata_agent, task_executor = setup
    mock_openai_chatcompletion_create.side_effect = params[
        "test_composite_eval_no_match"
    ]

    expected_actions = [
        EXPECTED_FUNCTION_ACTIONS[0],
        EXPECTED_CODE_ACTIONS[0],
    ]

    result = composite_evaluator.generate_eval_result(
        task, expected_actions, task_executor
    )

    assert result.full_match is False
    assert result.match_result == {
        EXPECTED_FUNCTION_ACTIONS[0]: False,
        EXPECTED_CODE_ACTIONS[0]: False,
    }
    assert result.extra_actions == [
        OpenAIFunctionCallAction(
            name="call_termination", arguments={"result": "Success"}
        )
    ]


def test_evaluation_harness_and_metrics(eval_harness, task, task2, setup):
    """Test the properties of EvaluationMetrics"""

    (
        mock_openai_chatcompletion_create,
        automata_agent,
        task_executor,
    ) = setup
    mock_openai_chatcompletion_create.side_effect = params[
        "test_evaluation_harness_and_metrics"
    ]

    expected_actions = [
        EXPECTED_FUNCTION_ACTIONS[0],
        EXPECTED_FUNCTION_ACTIONS[1],
        EXPECTED_CODE_ACTIONS[0],
        EXPECTED_CODE_ACTIONS[1],
    ]

    metrics = eval_harness.evaluate(
        [task, task2], expected_actions, task_executor
    )

    # Assert
    assert isinstance(metrics, EvaluationMetrics)
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
        {"call_termination({'result': 'Success'})": 2}
    )


def test_code_execution_error(composite_evaluator, task, setup):
    mock_openai_chatcompletion_create, automata_agent, task_executor = setup
    mock_openai_chatcompletion_create.side_effect = params[
        "test_composite_eval_no_match"
    ]

    expected_actions = [
        EXPECTED_FUNCTION_ACTIONS[0],
        EXPECTED_CODE_ACTIONS[0],
    ]

    result = composite_evaluator.generate_eval_result(
        task, expected_actions, task_executor
    )

    assert result.full_match is False
    assert result.match_result == {
        EXPECTED_FUNCTION_ACTIONS[0]: False,
        EXPECTED_CODE_ACTIONS[0]: False,
    }
    assert result.extra_actions == [
        OpenAIFunctionCallAction(
            name="call_termination", arguments={"result": "Success"}
        )
    ]


def test_task_evaluation_with_database_integration(
    setup_real, composite_evaluator, conversation_db, task_w_agent_session
):
    (
        mock_openai_chatcompletion_create,
        automata_agent,
        task_executor,
        real_registry,
    ) = setup_real

    mock_conversation = params["test_composite_eval_partial_match"]
    mock_openai_chatcompletion_create.side_effect = mock_conversation

    expected_actions = [
        EXPECTED_FUNCTION_ACTIONS[0],
        EXPECTED_CODE_ACTIONS[0],
    ]

    composite_evaluator.generate_eval_result(
        task_w_agent_session, expected_actions, task_executor
    )

    session_id = str(task_w_agent_session.session_id)
    fetched_task = real_registry.fetch_task_by_id(session_id)
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


# Standalone test for the EvalResultDatabase
def test_eval_result_writer(eval_db):
    # Generate a test EvalResult
    action1 = EXPECTED_CODE_ACTIONS[0]
    action2 = EXPECTED_CODE_ACTIONS[1]
    eval_result = EvalResult(
        full_match=True,
        match_result={action1: True, action2: False},
        extra_actions=[action2],
        session_id="test_session",
    )

    # Write the result to the database
    eval_db.write_result(eval_result, 1)

    # Retrieve the result from the database
    retrieved_results = eval_db.get_results("test_session")

    # Check that the retrieved result matches the original result
    assert len(retrieved_results) == 1
    retrieved_result = retrieved_results[0]
    assert retrieved_result.full_match == eval_result.full_match
    assert retrieved_result.match_result == eval_result.match_result
    assert retrieved_result.extra_actions == eval_result.extra_actions
    assert retrieved_result.session_id == eval_result.session_id
