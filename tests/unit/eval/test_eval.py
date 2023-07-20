from collections import Counter

import pytest

# from automata.agent import OpenAIAgentProvider, OpenAIAutomataAgent
# from automata.llm import OpenAIChatMessage, OpenAIConversation
# from automata.llm.eval.providers import (
#     OpenAIFunctionCallAction,
#     OpenAIFunctionEval,
# )

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
    conversation = mocker.MagicMock(spec=OpenAIConversation)
    eval_result = EvalResult(
        full_match=full_match,
        match_result=match_result,
        extra_actions=extra_actions,
        conversation=conversation,
    )
    assert eval_result.full_match == full_match
    assert eval_result.match_result == match_result
    assert eval_result.extra_actions == extra_actions
    assert eval_result.conversation == conversation


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
    mock_message.content = "```python\nz = 3.14```"

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
