import pytest

from automata.agent import OpenAIAgentProvider, OpenAIAutomataAgent
from automata.llm import OpenAIChatMessage, OpenAIConversation
from automata.llm.eval.providers import (
    OpenAIFunctionCallAction,
    OpenAIFunctionEval,
)


@pytest.fixture
def agent(mocker):
    agent = mocker.MagicMock(spec=OpenAIAutomataAgent)
    agent.run = mocker.MagicMock(return_value=None)
    agent.conversation = mocker.MagicMock(spec=OpenAIConversation)
    return agent


def test_generate_function_eval_result_match(agent, mocker):
    # Arrange
    expected_actions = [
        OpenAIFunctionCallAction(
            name="function1", arguments={"arg1": "value1"}
        ),
        OpenAIFunctionCallAction(
            name="function2", arguments={"arg2": "value2"}
        ),
    ]

    mock_message1 = mocker.MagicMock(spec=OpenAIChatMessage)
    mock_message1.function_call = OpenAIFunctionCallAction(
        name="function1", arguments={"arg1": "value1"}
    )

    mock_message2 = mocker.MagicMock(spec=OpenAIChatMessage)
    mock_message2.function_call = OpenAIFunctionCallAction(
        name="function2", arguments={"arg2": "value2"}
    )

    agent.conversation.messages = [mock_message1, mock_message2]
    provider = mocker.MagicMock(spec=OpenAIAgentProvider)
    provider.build_and_run_agent = mocker.MagicMock(return_value=agent)
    evaluator = OpenAIFunctionEval(provider)

    result = evaluator.generate_eval_result("instructions", expected_actions)

    assert result.full_match
    assert result.match_result == {action: True for action in expected_actions}
    assert result.extra_actions == []


def test_generate_eval_result_no_match(agent, mocker):
    # Arrange
    expected_actions = [
        OpenAIFunctionCallAction(
            name="function1", arguments={"arg1": "value1"}
        ),
        OpenAIFunctionCallAction(
            name="function2", arguments={"arg2": "value2"}
        ),
    ]

    mock_message = mocker.MagicMock(spec=OpenAIChatMessage)
    mock_message.function_call = OpenAIFunctionCallAction(
        name="function3", arguments={"arg3": "value3"}
    )

    agent.conversation.messages = [mock_message]

    provider = mocker.MagicMock(spec=OpenAIAgentProvider)
    provider.build_and_run_agent = mocker.MagicMock(return_value=agent)
    evaluator = OpenAIFunctionEval(provider)

    result = evaluator.generate_eval_result("instructions", expected_actions)

    assert not result.full_match
    assert result.match_result == {
        action: False for action in expected_actions
    }
    assert result.extra_actions == [
        OpenAIFunctionCallAction(
            name="function3", arguments={"arg3": "value3"}
        )
    ]


def test_generate_eval_result_partial_match(agent, mocker):
    # Arrange
    expected_actions = [
        OpenAIFunctionCallAction(
            name="function1", arguments={"arg1": "value1"}
        ),
        OpenAIFunctionCallAction(
            name="function2", arguments={"arg2": "value2"}
        ),
    ]

    mock_message = mocker.MagicMock(spec=OpenAIChatMessage)
    mock_message.function_call = OpenAIFunctionCallAction(
        name="function1", arguments={"arg1": "value1"}
    )

    agent.conversation.messages = [mock_message]

    provider = mocker.MagicMock(spec=OpenAIAgentProvider)
    provider.build_and_run_agent = mocker.MagicMock(return_value=agent)
    evaluator = OpenAIFunctionEval(provider)

    with mocker.patch(
        "automata.agent.providers.OpenAIAutomataAgent", return_value=agent
    ):
        result = evaluator.generate_eval_result(
            "instructions", expected_actions
        )

    assert not result.full_match
    assert result.match_result == {
        expected_actions[0]: True,
        expected_actions[1]: False,
    }
    assert result.extra_actions == []
