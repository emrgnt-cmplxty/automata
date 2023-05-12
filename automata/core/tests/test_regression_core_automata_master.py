import textwrap

import pytest

from automata.configs.config_enums import AgentConfigName

from .conftest import build_agent_with_params, cleanup_and_check

MODEL = "gpt-4"
TEMPERATURE = 0.7

# Stop the exmaples early to avoid random error
# Will be fixed once we set sub-models to T=0
EXPECTED_RESPONSES = {
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


@pytest.mark.regression
@pytest.mark.parametrize(
    "automata_params",
    [
        {
            "model": MODEL,
            "temperature": TEMPERATURE,
            "tool_list": ["automata_indexer", "automata_writer"],
            "exclude_overview": True,
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
        AgentConfigName.AUTOMATA_MASTER_PROD,
        max_iters=5,
    )

    agent.run()
    expected_content = EXPECTED_RESPONSES["test_retrieve_run_and_write_out"].strip()

    cleanup_and_check(expected_content, "test3.py")
