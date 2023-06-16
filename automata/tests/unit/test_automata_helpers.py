import textwrap

from automata.core.agent.actions import AutomataActionExtractor as ActionExtractor
from automata.core.agent.agent_utils import (
    generate_user_observation_message,
    retrieve_completion_message,
)
from automata.core.base.tool import ToolNotFoundError


def test_extract_actions_0():
    input_text = textwrap.dedent(
        """
        - thoughts
            - I will use the automata-indexer-retrieve-code tool to retrieve the code for the "run" function from the Automata agent.
        - actions
            - tool_query_0
                - tool_name
                    - automata-indexer-retrieve-code
                - tool_args
                    - Retrieve the raw code for the function 'run' from the Automata agent, including all necessary imports and docstrings.
        """
    )

    result = ActionExtractor.extract_actions(input_text)
    assert result[0].tool_name == "automata-indexer-retrieve-code"
    assert (
        result[0].tool_args[0]
        == "Retrieve the raw code for the function 'run' from the Automata agent, including all necessary imports and docstrings."
    )


def test_extract_actions_1():
    input_text = textwrap.dedent(
        """
        - thoughts
            - I will use the automata-indexer-retrieve-code tool to retrieve the code for the "run" function from the Automata agent.
        - actions
            - tool_query_0
                - tool_name
                    - automata-indexer-retrieve-code
                - tool_args
                    - Retrieve the raw code for the function 'run' from the Automata agent, including all necessary imports and docstrings.
            - tool_query_1
                - tool_name
                    - automata-writer-modify-module
                - tool_args
                    - Modify the code in the Automata agent.
                    - A dummy input....
        """
    )

    result = ActionExtractor.extract_actions(input_text)
    assert result[0].tool_name == "automata-indexer-retrieve-code"
    assert (
        result[0].tool_args[0]
        == "Retrieve the raw code for the function 'run' from the Automata agent, including all necessary imports and docstrings."
    )

    assert result[1].tool_name == "automata-writer-modify-module"
    assert result[1].tool_args[0] == "Modify the code in the Automata agent."

    assert result[1].tool_args[1] == "A dummy input...."


def test_extract_actions_2():
    input_text = textwrap.dedent(
        """
        - thoughts
            - I will use the automata-indexer-retrieve-code tool to retrieve the code for the "run" function from the Automata agent.
        - actions
            - tool_query_0
                - tool_name
                    - automata-indexer-retrieve-code
                - tool_args
                    - Retrieve the raw code for the function 'run' from the Automata agent, including all necessary imports and docstrings.
            - tool_query_1
                - tool_name
                    - automata-writer-modify-module
                - tool_args
                    - Modify the code in the Automata agent.
                    - python
                    ```
                    def f(x: int) -> int:
                        return 0
                    ```
        """
    )

    result = ActionExtractor.extract_actions(input_text)
    assert result[0].tool_name == "automata-indexer-retrieve-code"
    assert (
        result[0].tool_args[0]
        == "Retrieve the raw code for the function 'run' from the Automata agent, including all necessary imports and docstrings."
    )

    assert result[1].tool_name == "automata-writer-modify-module"
    assert result[1].tool_args[0] == "Modify the code in the Automata agent."

    assert result[1].tool_args[1] == "def f(x: int) -> int:\n    return 0\n"


def test_extract_actions_3():
    text = textwrap.dedent(
        """
        *Assistant*
            - thoughts
                - Having successfully written the output file, I can now return the result.
            - actions
                - return_result_0
                    - Function 'run' has been added to core.tests.sample_code.test.
        """
    )

    extractor = ActionExtractor()
    result = extractor.extract_actions(text)

    assert result[0].result_name == "return_result_0"
    assert (
        result[0].result_outputs[0]
        == "Function 'run' has been added to core.tests.sample_code.test."
    )


def test_extract_actions_4():
    text = textwrap.dedent(
        """
        *Assistant*
            - thoughts
                - Having successfully written the output file, I can now return the result.
            - actions
                - tool_query_0
                    - tool_name
                        - automata-indexer-retrieve-code
                    - tool_args
                        - Retrieve the raw code for the function 'run' from the Automata agent, including all necessary imports and docstrings.

                - return_result_0
                    - Function 'run' has been added to core.tests.sample_code.test.
        """
    )

    extractor = ActionExtractor()
    results = extractor.extract_actions(text)
    assert results[0].tool_name == "automata-indexer-retrieve-code"
    assert (
        results[0].tool_args[0]
        == "Retrieve the raw code for the function 'run' from the Automata agent, including all necessary imports and docstrings."
    )
    assert results[1].result_name == "return_result_0"
    assert (
        results[1].result_outputs[0]
        == "Function 'run' has been added to core.tests.sample_code.test."
    )


def test_extract_actions_5(automata_agent):
    text = textwrap.dedent(
        """
        - thoughts
            - Having successfully written the output file, I can now return the result.
        - actions
            - tool_query_0
                - tool_name
                    - automata-indexer-retrieve-code
                - tool_args
                    - Retrieve the raw code for the function 'run' from the Automata agent, including all necessary imports and docstrings.

            - return_result_0
                - Function 'run' has been added to core.tests.sample_code.test.
        """
    )
    processed_input = automata_agent._generate_observations(text)
    assert "%s" % (processed_input["tool_output_0"]) == "%s" % (
        ToolNotFoundError("automata-indexer-retrieve-code")
    )
    assert (
        processed_input["return_result_0"]
        == """Function 'run' has been added to core.tests.sample_code.test."""
    )


def test_extract_actions_6(automata_agent):
    text = textwrap.dedent(
        """
        - thoughts
            - Having successfully written the output file, I can now return the result.
        - actions
            - tool_query_0
                - tool_name
                    - automata-indexer-retrieve-code
                - tool_args
                    - Retrieve the raw code for the function 'run' from the Automata agent, including all necessary imports and docstrings.

            - return_result_0
                - Function 'run' has been added to core.tests.sample_code.test.
        """
    )
    observations = automata_agent._generate_observations(text)
    is_return_result = retrieve_completion_message(observations)

    user_observation_message = generate_user_observation_message(observations)
    assert is_return_result
    expected_observations = textwrap.dedent(
        """-  observations
    - tool_output_0
      - Error: Tool 'automata-indexer-retrieve-code' not found.
    - return_result_0
      - Function 'run' has been added to core.tests.sample_code.test.
        """
    )
    assert user_observation_message.strip() == expected_observations.strip()


def test_extract_actions_7():
    text = textwrap.dedent(
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
        """
    )
    actions = ActionExtractor.extract_actions(text)
    assert actions[0].tool_name == "python-indexer-retrieve-docstring"
    assert actions[0].tool_args == ["core.utils", "calculate_similarity"]

    assert actions[1].tool_name == "python-indexer-retrieve-code"
    assert actions[1].tool_args == ["core.utils", "calculate_similarity"]


def test_extract_actions_8():
    text = textwrap.dedent(
        """
    - thoughts
        - I will use the automata-indexer agent to retrieve the code for the "run" function from the class AutomataAgent.
    - actions
        - agent_query_1
            - agent_version
                - automata_indexer_dev
            - agent_instruction
                - Retrieve the code for the function 'run' from AutomataAgent, including all necessary imports and docstrings.
    """
    )
    actions = ActionExtractor.extract_actions(text)
    assert len(actions) == 1
