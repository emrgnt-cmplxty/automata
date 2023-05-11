import textwrap
from unittest.mock import MagicMock, patch

import pytest

from automata.configs.automata_agent_configs import AutomataAgentConfig
from automata.configs.config_enums import AgentConfigVersion
from automata.core.agent.automata_actions import AgentAction
from automata.core.agent.automata_agent_builder import AutomataAgentBuilder
from automata.core.agent.automata_agent_utils import build_agent_message
from automata.core.agent.tests.conftest import automata_agent as automata_agent_fixture  # noqa
from automata.core.coordinator.automata_coordinator import AutomataCoordinator, AutomataInstance


@pytest.fixture
def coordinator():  # noqa
    coordinator = AutomataCoordinator()
    return coordinator


@pytest.fixture
def main_agent(automata_agent_fixture, coordinator):  # noqa
    main_agent = automata_agent_fixture
    main_agent.set_coordinator(coordinator)
    return main_agent


# Mock AutomataInstance to be added to the coordinator
class MockAutomataInstance(AutomataInstance):
    def __init__(
        self,
        config_name: AgentConfigVersion,
        description: str,
    ):
        super().__init__(config_name=config_name, description=description)

    def run(self, instruction):
        return f"Running {instruction} on {self.config_name.value}."


@pytest.fixture
def coordinator_with_mock_agent():
    coordinator = AutomataCoordinator()
    mock_agent_instance = MockAutomataInstance(
        config_name=AgentConfigVersion.TEST,
        description="Mock agent for testing.",
    )
    coordinator.add_agent_instance(mock_agent_instance)
    return coordinator


def test_initialize_coordinator(coordinator):
    assert isinstance(coordinator, AutomataCoordinator)


def test_add_agent(coordinator):
    agent_builder = AutomataAgentBuilder
    agent_instance = AutomataInstance(config_name=AgentConfigVersion.TEST, builder=agent_builder)

    coordinator.add_agent_instance(agent_instance)
    assert len(coordinator.agent_instances) == 1


def test_set_coordinator_main(coordinator, main_agent):
    coordinator.set_main_agent(main_agent)
    main_agent.set_coordinator(coordinator)


def test_cannot_add_agent_twice(coordinator):
    agent_builder = AutomataAgentBuilder
    agent_instance = AutomataInstance(config_name=AgentConfigVersion.TEST, builder=agent_builder)

    coordinator.add_agent_instance(agent_instance)

    with pytest.raises(ValueError):
        coordinator.add_agent_instance(agent_instance)


def test_remove_agent(coordinator):
    agent_builder = AutomataAgentBuilder
    agent_instance = AutomataInstance(config_name=AgentConfigVersion.TEST, builder=agent_builder)

    coordinator.add_agent_instance(agent_instance)
    coordinator.remove_agent_instance(config_name=AgentConfigVersion.TEST)
    assert len(coordinator.agent_instances) == 0


def test_cannot_remove_missing_agent(coordinator):
    agent_builder = AutomataAgentBuilder
    agent_instance = AutomataInstance(config_name=AgentConfigVersion.TEST, builder=agent_builder)

    coordinator.add_agent_instance(agent_instance)
    with pytest.raises(ValueError):
        coordinator.remove_agent_instance(config_name=AgentConfigVersion.DEFAULT)


def test_add_agent_set_coordinator(coordinator, main_agent):
    agent_builder = AutomataAgentBuilder
    agent_instance = AutomataInstance(config_name=AgentConfigVersion.TEST, builder=agent_builder)
    coordinator.add_agent_instance(agent_instance)

    coordinator.set_main_agent(main_agent)
    main_agent.set_coordinator(coordinator)

    assert len(coordinator.agent_instances) == 1


def test_build_agent_message():
    agent_message = build_agent_message(
        {AgentConfigVersion.TEST: AutomataAgentConfig.load(AgentConfigVersion.TEST)}
    )
    assert agent_message == "\ntest: A test agent\n"


def mock_openai_response_with_agent_query():
    return {
        "choices": [
            {
                "message": {
                    "content": textwrap.dedent(
                        """
                        - thoughts
                            - I can retrieve this information directly with the python indexer.
                        - actions
                            - agent_query_0
                                - agent_version
                                    - test
                                - agent_instruction
                                    - Begin
                        """
                    )
                }
            }
        ]
    }


def mocked_execute_agent(_):
    response = textwrap.dedent(
        '''
        - thoughts
            - Having successfully written the output file, I can now return the result.
        - actions
            - return_result_0
                - This is a mock return result
        """
        '''
    )
    return response


@pytest.mark.parametrize("api_response", [mock_openai_response_with_agent_query()])
@patch("openai.ChatCompletion.create")
def test_iter_task_with_agent_query(
    mock_openai_chatcompletion_create, api_response, coordinator, main_agent
):
    mock_openai_chatcompletion_create.return_value = api_response

    coordinator.set_main_agent(main_agent)
    main_agent.set_coordinator(coordinator)

    main_agent._execute_agent = MagicMock(side_effect=mocked_execute_agent)

    main_agent.iter_task()

    completion_message = main_agent.messages[-1].content
    assert "- agent_output_0" in completion_message
    assert "- This is a mock return " in completion_message


def mock_openai_response_with_agent_query_and_tool_queries():
    return {
        "choices": [
            {
                "message": {
                    "content": textwrap.dedent(
                        """
                        - thoughts
                            - I can retrieve this information directly with the python indexer.
                        - actions
                            - tool_query_0
                                - tool_name
                                    - python-indexer-retrieve-docstring
                                - tool_args
                                    - core.utils
                                    - calculate_similarity
                            - tool_query_1
                                - tool_name
                                    - python-indexer-retrieve-code
                                - tool_args
                                    - core.utils
                                    - calculate_similarity
                            - agent_query_1
                                - agent_version
                                    - test
                                - agent_instruction
                                    - Begin
                        """
                    )
                }
            }
        ]
    }


@pytest.mark.parametrize(
    "api_response", [mock_openai_response_with_agent_query_and_tool_queries()]
)
@patch("openai.ChatCompletion.create")
def test_iter_task_with_agent_and_tool_query(
    mock_openai_chatcompletion_create, api_response, coordinator, main_agent
):
    coordinator.set_main_agent(main_agent)
    main_agent.set_coordinator(coordinator)
    mock_openai_chatcompletion_create.return_value = api_response

    main_agent._execute_agent = MagicMock(side_effect=mocked_execute_agent)

    main_agent.iter_task()

    completion_message = main_agent.messages[-1].content
    assert "- tool_output_0" in completion_message
    assert "- tool_output_1" in completion_message
    assert "- agent_output_1" in completion_message
    assert "- This is a mock return " in completion_message


@pytest.mark.parametrize("api_response", [mock_openai_response_with_agent_query()])
@patch("openai.ChatCompletion.create")
def test_iter_task_with_agent_and_tool_query_2(
    mock_openai_chatcompletion_create, api_response, coordinator, main_agent
):
    coordinator.set_main_agent(main_agent)
    main_agent.set_coordinator(coordinator)
    mock_openai_chatcompletion_create.return_value = api_response

    main_agent._execute_agent = MagicMock(side_effect=mocked_execute_agent)

    main_agent.iter_task()

    completion_message = main_agent.messages[-1].content
    assert "- agent_output_0" in completion_message
    assert "- This is a mock return " in completion_message


def mock_openai_response_with_agent_query_1():
    return {
        "choices": [
            {
                "message": {
                    "content": textwrap.dedent(
                        """
                        - thoughts
                            - I can retrieve this information directly with the python indexer.
                        - actions
                        - agent_query_1
                            - agent_version
                                - test
                            - agent_instruction
                                - Begin
                        """
                    )
                }
            }
        ]
    }


@pytest.mark.parametrize("api_response", [mock_openai_response_with_agent_query_1()])
@patch("openai.ChatCompletion.create")
def test_iter_task_with_agent_and_tool_query_3(
    mock_openai_chatcompletion_create, api_response, coordinator, main_agent
):
    coordinator.set_main_agent(main_agent)
    main_agent.set_coordinator(coordinator)
    mock_openai_chatcompletion_create.return_value = api_response

    main_agent._execute_agent = MagicMock(side_effect=mocked_execute_agent)

    main_agent.iter_task()

    completion_message = main_agent.messages[-1].content
    assert "- agent_output_1" in completion_message
    assert "- This is a mock return " in completion_message


# Test the run_agent function of the coordinator
def test_run_agent(coordinator_with_mock_agent, main_agent):
    coordinator = coordinator_with_mock_agent
    coordinator.set_main_agent(main_agent)
    main_agent.set_coordinator(coordinator)
    action = AgentAction(
        agent_version=AgentConfigVersion.TEST,
        agent_query="mock_agent_query",
        agent_instruction=["Test instruction."],
    )
    result = coordinator.run_agent(action)
    assert result == "Running Test instruction. on test."


# Test the _execute_agent method of MasterAutomataAgent
def test_execute_agent(automata_agent_fixture, coordinator_with_mock_agent):  # noqa
    # Set up MasterAutomataAgent and Coordinator
    main_agent = automata_agent_fixture
    main_agent.set_coordinator(coordinator_with_mock_agent)

    # Create a mock AgentAction
    mock_agent_action = AgentAction(
        agent_version=AgentConfigVersion.TEST,
        agent_instruction="Test instruction.",
        agent_query="AutomataAgentBuilder",
    )

    # Mock the run_agent method of the coordinator
    coordinator_with_mock_agent.run_agent = MagicMock()

    # Call _execute_agent with the mock_agent_action
    main_agent._execute_agent(mock_agent_action)

    # Assert that the run_agent method of the coordinator was called with correct arguments
    coordinator_with_mock_agent.run_agent.assert_called_with(mock_agent_action)
