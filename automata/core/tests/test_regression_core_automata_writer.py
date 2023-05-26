import textwrap

import pytest

from automata.configs.config_enums import AgentConfigName

from .conftest import build_agent_with_params, cleanup_and_check

MODEL = "gpt-4"
TEMPERATURE = 0.7

# Stop the exmaples early to avoid random error
# Will be fixed once we set sub-models to T=0
EXPECTED_RESPONSES = {
    "test_write_simple_function": "def test_write_simple_response(automata_writer_params) -> bool:\n    return True",
    "test_advanced_writer_example": textwrap.dedent(
        '''
        """This is a sample module for testing"""


        def test_function() -> bool:
            """This is my new function"""
            return True


        class TestClass:
            """This is my test class"""

            def __init__(self):
                """This initializes TestClass"""
                pass

            def test_method(self) -> bool:
                """This is my test method"""
                return False
        '''
    ),
}


@pytest.mark.regression
@pytest.mark.parametrize(
    "automata_params",
    [
        {
            "model": MODEL,
            "temperature": TEMPERATURE,
            "tool_list": ["python_writer", "python_inspector"],
        },
        # Add more parameter sets as needed
    ],
    indirect=True,
)
def test_write_simple_function(automata_params):
    expected_content = EXPECTED_RESPONSES["test_write_simple_function"].strip()
    agent = build_agent_with_params(
        automata_params,
        f"Write the following function - '{expected_content}' to the file core.tests.sample_code.test",
        AgentConfigName.AUTOMATA_WRITER_PROD,
        max_iters=5,
        temperature=TEMPERATURE,
        model=MODEL,
    )
    agent.run()
    cleanup_and_check(expected_content, "test.py")


@pytest.mark.regression
@pytest.mark.parametrize(
    "automata_params",
    [
        {
            "model": MODEL,
            "temperature": TEMPERATURE,
            "tool_list": ["python_inspector", "python_writer"],
        },
        # Add more parameter sets as needed
    ],
    indirect=True,
)
def test_advanced_writer_example(automata_params):
    expected_content = EXPECTED_RESPONSES["test_advanced_writer_example"].strip()
    agent = build_agent_with_params(
        automata_params,
        f"Write the following module - '{expected_content}' to the file core.tests.sample_code.test2",
        AgentConfigName.AUTOMATA_WRITER_PROD,
        max_iters=2,
        temperature=TEMPERATURE,
        model=MODEL,
    )
    agent.run()
    cleanup_and_check(expected_content, "test2.py")
