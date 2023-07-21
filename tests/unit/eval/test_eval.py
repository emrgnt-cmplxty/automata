from unittest.mock import MagicMock

import pytest

from automata.llm.eval import (
    CodeWritingAction,
    CodeWritingEval,
    CompositeEval,
    EvaluationHarness,
    OpenAIFunctionCallAction,
    OpenAIFunctionEval,
)
from automata.tasks.base import TaskStatus
from automata.tasks.executor import (
    AutomataTaskExecutor,
    IAutomataTaskExecution,
)


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


import os

from automata.memory_store import OpenAIAutomataConversationDatabase


@pytest.fixture(scope="module", autouse=True)
def db(tmpdir_factory):
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


EXPECTED_FUNCTION_ACTIONS = [
    OpenAIFunctionCallAction(name="function1", arguments={"arg1": "value1"}),
    OpenAIFunctionCallAction(name="function2", arguments={"arg2": "value2"}),
]


EXPECTED_CODE_ACTIONS = [
    CodeWritingAction(object_types="int", object_value=1),
    CodeWritingAction(object_types="str", object_value="test"),
]


@pytest.fixture
def setup(mocker, automata_agent, task, environment, registry, db):
    # Mock the API response
    mock_openai_chatcompletion_create = mocker.patch(
        "openai.ChatCompletion.create"
    )

    # Register and setup task
    registry.register(task)
    environment.setup(task)

    # Use the agent's set_database_provider method
    automata_agent.set_database_provider(db)

    execution = IAutomataTaskExecution()
    IAutomataTaskExecution._build_agent = MagicMock(
        return_value=automata_agent
    )
    task_executor = AutomataTaskExecutor(execution)

    return mock_openai_chatcompletion_create, automata_agent, task_executor


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
}


def test_generate_function_eval_result_match(db, task, evaluator, setup):
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
    assert task.result == "Execution Result:\n\nSuccess"

    saved_messages = db.get_messages(automata_agent.session_id)
    assert len(saved_messages) == 6


def test_generate_eval_result_no_match(db, task, evaluator, setup):
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


def test_generate_eval_result_partial_match(db, task, evaluator, setup):
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
    db, task, code_evaluator, setup
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
        CodeWritingAction(object_value=3.14, object_types="float")
    ]


def test_generate_code_writing_eval_result_no_match(
    db, task, code_evaluator, setup
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
    db, task, code_evaluator, setup
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


def test_composite_eval_result_match(db, task, composite_evaluator, setup):
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
        CodeWritingAction(object_value=3.14, object_types="float"),
    ]


def test_generate_code_writing_eval_result_partial_match(
    db, task, code_evaluator, setup
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


def test_composite_eval_partial_match(db, task, composite_evaluator, setup):
    mock_openai_chatcompletion_create, automata_agent, task_executor = setup
    mock_openai_chatcompletion_create.side_effect = params[
        "test_composite_eval_partial_match"
    ]

    expected_actions = [
        EXPECTED_FUNCTION_ACTIONS[0],
        EXPECTED_CODE_ACTIONS[0],
    ]

    result = composite_evaluator.generate_eval_result(
        task, expected_actions, task_executor
    )

    assert result.full_match == False
    print("result.match_result = ", result.match_result)
    assert result.match_result == {
        EXPECTED_FUNCTION_ACTIONS[0]: True,
        EXPECTED_CODE_ACTIONS[0]: False,
    }
    assert result.extra_actions == [
        OpenAIFunctionCallAction(
            name="call_termination", arguments={"result": "Success"}
        )
    ]


def test_composite_eval_no_match(db, task, composite_evaluator, setup):
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

    assert result.full_match == False
    assert result.match_result == {
        EXPECTED_FUNCTION_ACTIONS[0]: False,
        EXPECTED_CODE_ACTIONS[0]: False,
    }
    assert result.extra_actions == [
        OpenAIFunctionCallAction(
            name="call_termination", arguments={"result": "Success"}
        )
    ]


# def test_evaluation_harness_and_metrics(agent, eval_harness, mocker):
#     """Test the properties of EvaluationMetrics"""
#     # Arrange
#     function_call_action1 = OpenAIFunctionCallAction(
#         name="function1", arguments={"arg1": "value1"}
#     )
#     function_call_action2 = OpenAIFunctionCallAction(
#         name="function2", arguments={"arg2": "value2"}
#     )
#     code_writer_1 = CodeWritingAction(object_types="str", object_value="test")
#     code_writer_extra = CodeWritingAction(object_types="int", object_value="1")
#     expected_actions = [
#         [function_call_action1, function_call_action2],
#         [code_writer_1],
#     ]

#     # Only the first action is performed
#     mock_message1 = mocker.MagicMock(spec=OpenAIChatMessage)
#     mock_message1.function_call = function_call_action1
#     mock_message1.content = None

#     # The second action is not performed
#     mock_message2 = mocker.MagicMock(spec=OpenAIChatMessage)
#     mock_message2.function_call = None
#     mock_message2.content = (
#         "```python\nx = 1```"  # An unexpected code writing action
#     )

#     agent.conversation.messages = [mock_message1, mock_message2]

#     # Act
#     metrics = eval_harness.evaluate(
#         ["instruction1", "instruction2"], expected_actions
#     )
#     # Assert
#     assert isinstance(metrics, EvaluationMetrics)
#     assert metrics.total_actions == 3
#     assert metrics.total_successful_actions == 1
#     assert metrics.action_success_rate == 0.3333333333333333
#     assert metrics.total_extra_actions == 1
#     assert metrics.successful_actions_frequency == Counter(
#         {str(function_call_action1): 1}
#     )
#     assert metrics.failed_actions_frequency == Counter(
#         {str(function_call_action2): 1, str(code_writer_1): 1}
#     )
#     assert metrics.extra_action_frequency == Counter(
#         {str(code_writer_extra): 1}
#     )


# def test_code_execution_error(code_evaluator, agent, mocker):
#     """Test if CodeExecutionError is raised when there's an error in executing the code"""
#     # Arrange
#     mock_message = mocker.MagicMock(spec=OpenAIChatMessage)
#     mock_message.content = (
#         "```python\nx = 1/0```"  # This should raise a ZeroDivisionError
#     )
#     agent.conversation.messages = [mock_message]

#     expected_actions = [CodeWritingAction(object_types="int", object_value=1)]

#     # Act and Assert
#     with pytest.raises(CodeExecutionError):
#         code_evaluator.generate_eval_result("instructions", expected_actions)


# def mock_openai_response_with_function_completion_message():
#     return {
#         "choices": [
#             {
#                 "message": {
#                     "role": "assistant",
#                     "function_call": {
#                         "name": "call_termination",
#                         "arguments": '{"result": "Success"}',
#                     },
#                     "content": None,
#                 }
#             }
#         ]
#     }


# @pytest.mark.parametrize(
#     "api_response", [mock_openai_response_with_function_completion_message()]
# )
# @patch("openai.ChatCompletion.create")
# def test_task_evaluation_with_database_integration(
#     mock_openai_chatcompletion_create,
#     api_response,
#     automata_agent,
#     task,
#     environment,
#     registry,
#     mocker,
# ):
#     # Mock the API response
#     mock_openai_chatcompletion_create.return_value = api_response

#     # Generate a unique session ID for this test case
#     session_id = task.session_id

#     # Instantiate the three databases with the session ID
#     task_db = AutomataAgentTaskDatabase()
#     conversation_db = OpenAIAutomataConversationDatabase()
#     eval_db = EvalResultWriter()

#     # Create a task and set record_conversation to True
#     registry.register(task)
#     environment.setup(task)

#     # Connect the agent to the conversation and task databases
#     automata_agent.set_database_provider(conversation_db)
#     automata_agent.set_task_database(task_db)

#     # Create the evaluation harness with the task's expected actions
#     eval_harness = EvaluationHarness(task.expected_actions)

#     # Execute the task
#     execution = IAutomataTaskExecution()
#     IAutomataTaskExecution._build_agent = MagicMock(
#         return_value=automata_agent
#     )
#     task_executor = AutomataTaskExecutor(execution)
#     task_executor.execute(task)

#     # Retrieve the executed actions from the conversation database
#     executed_actions = conversation_db.get_actions_for_session(session_id)

#     # Evaluate the actions
#     metrics = eval_harness.evaluate(task.instructions, executed_actions)

#     # Store the evaluation results in the evaluation database
#     eval_db.write_result(session_id, metrics, task.conversation_id)

#     # Assert the task execution and evaluation results
#     assert task.status == TaskStatus.SUCCESS
#     assert task.result == "Execution Result:\n\nSuccess"

#     saved_messages = conversation_db.get_messages_for_session(session_id)
#     assert len(saved_messages) == len(task.instructions)

#     eval_results = eval_db.get_results(session_id)
#     assert len(eval_results) == 1  # Only one evaluation result should exist

#     # Other assertions to check the correctness of the evaluation can be added here...
