from collections import Counter

import pytest

from automata.agent import OpenAIAgentProvider, OpenAIAutomataAgent
from automata.llm import OpenAIChatMessage, OpenAIConversation
from automata.llm.eval import (
    CodeWritingAction,
    CodeWritingEval,
    CompositeEval,
    EvalResult,
    EvaluationHarness,
    EvaluationMetrics,
    OpenAIFunctionCallAction,
    OpenAIFunctionEval,
)
from automata.llm.eval.code_writing import CodeExecutionError


@pytest.fixture
def agent(mocker):
    agent = mocker.MagicMock(spec=OpenAIAutomataAgent)
    agent.run = mocker.MagicMock(return_value=None)
    agent.conversation = mocker.MagicMock(spec=OpenAIConversation)
    return agent


@pytest.fixture
def provider(agent, mocker):
    provider = mocker.MagicMock(spec=OpenAIAgentProvider)
    provider.build_and_run_agent = mocker.MagicMock(return_value=agent)
    return provider


@pytest.fixture
def evaluator(agent, provider):
    return OpenAIFunctionEval(provider)


@pytest.fixture
def code_evaluator(agent, provider):
    return CodeWritingEval(provider, target_variables=["x", "y", "z"])


@pytest.fixture
def composite_evaluator(agent, provider):
    evaluators = [OpenAIFunctionEval, CodeWritingEval]
    return CompositeEval(provider, evaluators)


@pytest.fixture
def eval_harness(evaluator, code_evaluator):
    return EvaluationHarness([evaluator, code_evaluator])


EXPECTED_ACTIONS = [
    OpenAIFunctionCallAction(name="function1", arguments={"arg1": "value1"}),
    OpenAIFunctionCallAction(name="function2", arguments={"arg2": "value2"}),
]


def test_eval_result_init(mocker):
    full_match = True
    match_result = {"action": True}
    extra_actions = ["action"]
    eval_result = EvalResult(
        full_match=full_match,
        match_result=match_result,
        extra_actions=extra_actions,
        session_id=None,
    )
    assert eval_result.full_match == full_match
    assert eval_result.match_result == match_result
    assert eval_result.extra_actions == extra_actions


def test_generate_function_eval_result_match(agent, evaluator, mocker):
    # Arrange
    mock_message1 = mocker.MagicMock(spec=OpenAIChatMessage)
    mock_message1.function_call = EXPECTED_ACTIONS[0]

    mock_message2 = mocker.MagicMock(spec=OpenAIChatMessage)
    mock_message2.function_call = EXPECTED_ACTIONS[1]

    agent.conversation.messages = [mock_message1, mock_message2]

    # Act
    result = evaluator.generate_eval_result("instructions", EXPECTED_ACTIONS)

    # Assert
    assert result.full_match
    assert result.match_result == {action: True for action in EXPECTED_ACTIONS}
    assert result.extra_actions == []


def test_generate_eval_result_no_match(agent, evaluator, mocker):
    # Arrange
    mock_message = mocker.MagicMock(spec=OpenAIChatMessage)
    mock_message.function_call = OpenAIFunctionCallAction(
        name="function3", arguments={"arg3": "value3"}
    )

    agent.conversation.messages = [mock_message]

    # Act
    result = evaluator.generate_eval_result("instructions", EXPECTED_ACTIONS)

    # Assert
    assert not result.full_match
    assert result.match_result == {
        action: False for action in EXPECTED_ACTIONS
    }
    assert result.extra_actions == [mock_message.function_call]


def test_generate_eval_result_partial_match(agent, evaluator, mocker):
    # Arrange
    mock_message = mocker.MagicMock(spec=OpenAIChatMessage)
    mock_message.function_call = EXPECTED_ACTIONS[0]

    agent.conversation.messages = [mock_message]

    # Act
    result = evaluator.generate_eval_result("instructions", EXPECTED_ACTIONS)

    # Assert
    assert not result.full_match
    assert result.match_result == {
        EXPECTED_ACTIONS[0]: True,
        EXPECTED_ACTIONS[1]: False,
    }
    assert result.extra_actions == []


def test_generate_code_writing_eval_result_match(
    agent, code_evaluator, mocker
):
    # Arrange
    mock_message1 = mocker.MagicMock(spec=OpenAIChatMessage)
    mock_message1.content = "```python\nx = 1```"

    mock_message2 = mocker.MagicMock(spec=OpenAIChatMessage)
    mock_message2.content = "```python\ny = 'test'```"

    agent.conversation.messages = [mock_message1, mock_message2]

    expected_actions = [
        CodeWritingAction(object_types="int", object_value=1),
        CodeWritingAction(object_types="str", object_value="test"),
    ]

    # Act
    result = code_evaluator.generate_eval_result(
        "instructions", expected_actions
    )

    # Assert
    assert result.full_match
    assert result.match_result == {action: True for action in expected_actions}
    assert result.extra_actions == []


def test_generate_code_writing_eval_result_no_match(
    agent, code_evaluator, mocker
):
    # Arrange
    mock_message = mocker.MagicMock(spec=OpenAIChatMessage)
    mock_message.content = "```python\nz = 3.14```"

    agent.conversation.messages = [mock_message]

    expected_actions = [
        CodeWritingAction(object_types="int", object_value=1),
        CodeWritingAction(object_types="str", object_value="test"),
    ]

    # Act
    result = code_evaluator.generate_eval_result(
        "instructions", expected_actions
    )

    # Assert
    assert not result.full_match
    assert result.match_result == {
        action: False for action in expected_actions
    }
    assert result.extra_actions == [
        CodeWritingAction(object_types="float", object_value=3.14)
    ]


def test_generate_code_writing_eval_result_partial_match(
    agent, code_evaluator, mocker
):
    # Arrange
    mock_message = mocker.MagicMock(spec=OpenAIChatMessage)
    mock_message.content = "```python\nx = 1```"

    agent.conversation.messages = [mock_message]

    expected_actions = [
        CodeWritingAction(object_types="int", object_value=1),
        CodeWritingAction(object_types="str", object_value="test"),
    ]

    # Act
    result = code_evaluator.generate_eval_result(
        "instructions", expected_actions
    )

    # Assert
    assert not result.full_match
    assert result.match_result == {
        expected_actions[0]: True,
        expected_actions[1]: False,
    }
    assert result.extra_actions == []


def test_composite_eval_result_match(agent, composite_evaluator, mocker):
    # Arrange
    function_call_action = OpenAIFunctionCallAction(
        name="function1", arguments={"arg1": "value1"}
    )
    code_writing_action = CodeWritingAction(object_types="int", object_value=1)

    mock_message1 = mocker.MagicMock(spec=OpenAIChatMessage)
    mock_message1.function_call = function_call_action
    mock_message1.content = None

    mock_message2 = mocker.MagicMock(spec=OpenAIChatMessage)
    mock_message2.content = "```python\nx = 1```"
    mock_message2.function_call = None

    agent.conversation.messages = [mock_message1, mock_message2]

    expected_actions = [function_call_action, code_writing_action]

    # Act
    result = composite_evaluator.generate_eval_results(
        "instructions", expected_actions
    )

    # Assert
    assert result.full_match
    assert result.match_result == {
        function_call_action: True,
        code_writing_action: True,
    }
    assert result.extra_actions == []


def test_composite_eval_result_partial_match(
    agent, composite_evaluator, mocker
):
    # Arrange
    function_call_action = OpenAIFunctionCallAction(
        name="function1", arguments={"arg1": "value1"}
    )
    code_writing_action = CodeWritingAction(object_types="int", object_value=1)

    # Only the function call action is performed, not the code writing action
    mock_message = mocker.MagicMock(spec=OpenAIChatMessage)
    mock_message.function_call = function_call_action
    mock_message.content = None

    agent.conversation.messages = [mock_message]

    expected_actions = [function_call_action, code_writing_action]

    # Act
    result = composite_evaluator.generate_eval_results(
        "instructions", expected_actions
    )

    # Assert
    assert not result.full_match
    # Check that the function call action matched but the code writing action did not
    assert result.match_result == {
        function_call_action: True,
        code_writing_action: False,
    }
    assert result.extra_actions == []


def test_composite_eval_result_no_match(agent, composite_evaluator, mocker):
    # Arrange
    function_call_action = OpenAIFunctionCallAction(
        name="function1", arguments={"arg1": "value1"}
    )
    code_writing_action = CodeWritingAction(object_types="int", object_value=1)

    # No function call or code writing actions are performed
    mock_message = mocker.MagicMock(spec=OpenAIChatMessage)
    mock_message.function_call = None
    mock_message.content = None

    agent.conversation.messages = [mock_message]

    expected_actions = [function_call_action, code_writing_action]

    # Act
    result = composite_evaluator.generate_eval_results(
        "instructions", expected_actions
    )

    # Assert
    assert not result.full_match
    # Check that neither action matched
    assert result.match_result == {
        function_call_action: False,
        code_writing_action: False,
    }
    assert result.extra_actions == []


def test_evaluation_harness_and_metrics(agent, eval_harness, mocker):
    """Test the properties of EvaluationMetrics"""
    # Arrange
    function_call_action1 = OpenAIFunctionCallAction(
        name="function1", arguments={"arg1": "value1"}
    )
    function_call_action2 = OpenAIFunctionCallAction(
        name="function2", arguments={"arg2": "value2"}
    )
    code_writer_1 = CodeWritingAction(object_types="str", object_value="test")
    code_writer_extra = CodeWritingAction(object_types="int", object_value="1")
    expected_actions = [
        [function_call_action1, function_call_action2],
        [code_writer_1],
    ]

    # Only the first action is performed
    mock_message1 = mocker.MagicMock(spec=OpenAIChatMessage)
    mock_message1.function_call = function_call_action1
    mock_message1.content = None

    # The second action is not performed
    mock_message2 = mocker.MagicMock(spec=OpenAIChatMessage)
    mock_message2.function_call = None
    mock_message2.content = (
        "```python\nx = 1```"  # An unexpected code writing action
    )

    agent.conversation.messages = [mock_message1, mock_message2]

    # Act
    metrics = eval_harness.evaluate(
        ["instruction1", "instruction2"], expected_actions
    )
    # Assert
    assert isinstance(metrics, EvaluationMetrics)
    assert metrics.total_actions == 3
    assert metrics.total_successful_actions == 1
    assert metrics.action_success_rate == 0.3333333333333333
    assert metrics.total_extra_actions == 1
    assert metrics.successful_actions_frequency == Counter(
        {str(function_call_action1): 1}
    )
    assert metrics.failed_actions_frequency == Counter(
        {str(function_call_action2): 1, str(code_writer_1): 1}
    )
    assert metrics.extra_action_frequency == Counter(
        {str(code_writer_extra): 1}
    )


def test_code_execution_error(code_evaluator, agent, mocker):
    """Test if CodeExecutionError is raised when there's an error in executing the code"""
    # Arrange
    mock_message = mocker.MagicMock(spec=OpenAIChatMessage)
    mock_message.content = (
        "```python\nx = 1/0```"  # This should raise a ZeroDivisionError
    )
    agent.conversation.messages = [mock_message]

    expected_actions = [CodeWritingAction(object_types="int", object_value=1)]

    # Act and Assert
    with pytest.raises(CodeExecutionError):
        code_evaluator.generate_eval_result("instructions", expected_actions)


def mock_openai_response_with_completion_message():
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


# @pytest.mark.parametrize(
#     "api_response", [mock_openai_response_with_completion_message()]
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
