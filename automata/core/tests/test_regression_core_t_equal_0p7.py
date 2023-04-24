import textwrap

import pytest

from automata.configs.agent_configs import AgentConfig

from .conftest import build_agent_with_params, cleanup_and_check, retry

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
    "test_retrieve_run_and_write_out": textwrap.dedent(
        """
        def run(self) -> str:
            while True:
                self.iter_task()
                if AutomataAgent.is_completion_message(self.messages[-2]["content"]):
                    return self.messages[-2]["content"]
                if (len(self.messages) - AutomataAgent.NUM_DEFAULT_MESSAGES) >= self.max_iters * 2:
                    return "Result was not captured before iterations exceeded max limit."
        """
    ),
}


@retry(3)
@pytest.mark.regression
@pytest.mark.parametrize(
    "automata_params",
    [
        {
            "model": MODEL,
            "temperature": TEMPERATURE,
            "tool_list": ["automata_indexer", "automata_writer"],
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
        AgentConfig.AUTOMATA_WRITER_V2,
        max_iters=5,
        temperature=TEMPERATURE,
        model=MODEL,
    )
    agent.run()
    cleanup_and_check(expected_content, "test.py")


@retry(3)
@pytest.mark.regression
@pytest.mark.parametrize(
    "automata_params",
    [
        {
            "model": MODEL,
            "temperature": TEMPERATURE,
            "tool_list": ["python_indexer", "python_writer"],
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
        config=AgentConfig.AUTOMATA_WRITER_V2,
        max_iters=2,
        temperature=TEMPERATURE,
        model=MODEL,
    )
    agent.run()
    cleanup_and_check(expected_content, "test2.py")


@retry(3)
@pytest.mark.regression
@pytest.mark.parametrize(
    "automata_params",
    [
        {
            "model": MODEL,
            "temperature": TEMPERATURE,
            "tool_list": ["automata_indexer", "automata_writer"],
        },
        # Add more parameter sets as needed
    ],
    indirect=True,
)
# TODO - Understand why the docstring is omitted by the agent, and find a simple fix.
def test_retrieve_run_and_write_out(automata_params):
    agent = build_agent_with_params(
        automata_params,
        f'1. Retrieve the raw code (code + docstrings) for the function "run" from the automata agent.\n'
        f"2. NEXT, write the full raw code into the file core.tests.sample_code.test3",
        config=AgentConfig.AUTOMATA_MASTER_V3,
        max_iters=5,
    )

    next_steps = (
        {
            "role": "assistant",
            "content": 'Thought: I will use the automata-indexer-retrieve-code tool to retrieve the raw code for the "run" function from the Automata agent.\nAction:\n{\n  "tool": "automata-indexer-retrieve-code",\n  "input": "Retrieve the raw code for the function \'run\' from the Automata agent, including all necessary imports and docstrings."\n}',
        },
        {
            "role": "user",
            "content": """Observation:\n{\n"output_0": "def run(self) -> str:\n    \\"\\"\\"Run until the initial instruction terminates.\\"\\"\\"\n    while True:\n        self.iter_task()\n        if AutomataAgent.is_completion_message(self.messages[-2][\'content\']):\n            return self.messages[-2][\'content\']\n        if len(self.messages) - AutomataAgent.NUM_DEFAULT_MESSAGES >= self.max_iters * 2:\n            return \'Result was not captured before iterations exceeded max limit.\'"", \n}"printObservation:\n{\n\"output_0\": \"The code for the 'run' function in Automata agent is:\n\ndef run(self) -> str:\n    while True:\n        self.iter_task()\n        if AutomataAgent.is_completion_message(self.messages[-2]['content']):\n            return self.messages[-2]['content']\n        if len(self.messages) - AutomataAgent.NUM_DEFAULT_MESSAGES >= self.max_iters * 2:\n            return 'Result was not captured before iterations exceeded max limit.'\n\nNote: No docstring was found for this function.\"\", \n}""",
        },
    )
    agent.messages.extend(next_steps)
    agent.run()
    print("agent.messages = ", agent.messages)

    expected_content = EXPECTED_RESPONSES["test_retrieve_run_and_write_out"].strip()
    print("expected_content = ", expected_content)

    cleanup_and_check(expected_content, "test3.py")
