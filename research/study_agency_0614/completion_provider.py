"""Module for the completion provider"""
import textwrap
from enum import Enum
from typing import List, Optional, Tuple

from constants import (
    ADVANCED_SYSTEM_PROMPT,
    BAD_SYSTEM_PROMPT,
    VANILLA_SYSTEM_PROMPT,
)

from automata.agent import OpenAIAutomataAgent
from automata.config import OpenAIAutomataAgentConfigBuilder
from automata.llm import OpenAIChatCompletionProvider, OpenAIConversation
from automata.tools import Tool


class RunMode(Enum):
    """Specifies the mode of running the completion provider"""

    VANILLA = "vanilla"
    VANILLA_AGENT_RETURN_ONLY = "vanilla-agent-return-only"
    ADVANCED_AGENT_RETURN_ONLY = "advanced-agent-return-only"
    BAD_AGENT_RETURN_ONLY = "bad-agent-return-only"

    ADVANCED_AGENT_INTERPRETER = "advanced-agent-with-interpreter"


class CompletionProvider:
    """Concrete class for completion providers"""

    def __init__(self, run_mode: RunMode, model: str, temperature: float):
        self.run_mode = run_mode
        self.model = model
        self.temperature = temperature

    def get_raw_and_cleaned_completions(
        self, raw_prompt: str
    ) -> Tuple[str, str]:
        """Returns the raw and cleaned completions for the given prompt"""
        if self.run_mode == RunMode.VANILLA:
            vanilla_instructions = self.get_formatted_instruction(raw_prompt)
            raw_completion = self.generate_vanilla_completion(
                vanilla_instructions
            )
        else:
            vanilla_system_prompt = self.get_system_prompt()
            vanilla_instructions = self.get_formatted_instruction(raw_prompt)
            raw_completion = self.generate_agent_completion(
                vanilla_system_prompt, vanilla_instructions
            )
        clean_completion = self.extract_code(raw_completion)
        return (raw_completion, clean_completion)

    def generate_vanilla_completion(self, instructions: str) -> str:
        """Generates a vanilla completion for the given prompt"""
        provider = OpenAIChatCompletionProvider(
            model=self.model,
            temperature=self.temperature,
            stream=True,
            conversation=OpenAIConversation(),
            functions=[],
        )
        return provider.standalone_call(instructions)

    def generate_agent_completion(
        self,
        system_prompt: str,
        instructions: str,
        tools: Optional[List[Tool]] = None,
    ) -> str:
        """Generates an agent completion for the given prompt"""
        if not tools:
            tools = []

        config_builder = (
            OpenAIAutomataAgentConfigBuilder()
            .with_stream(True)
            .with_verbose(True)
            .with_tools(tools)  # type: ignore
            .with_system_template(system_prompt)
            .with_model(self.model)
            .with_temperature(self.temperature)
        )

        if self.run_mode == RunMode.BAD_AGENT_RETURN_ONLY:
            config_builder = config_builder.with_instruction_version(  # type: ignore
                "bad-introduction"
            )

        agent = OpenAIAutomataAgent(instructions, config_builder.build())

        try:
            return agent.run()
        except Exception as e:
            return f"Exception {e} occurred while running."

    def extract_code(self, raw_completion: str) -> str:
        """Extracts the markdown snippet from the raw completion"""
        # Extract the markdown snippet for results like '```python ...```'
        # or '```....```'
        clean_completion = (
            raw_completion.split("```python")[1].split("```")[0]
            if "```python" in raw_completion
            else raw_completion
        )
        clean_completion = (
            clean_completion.split("```")[1].split("```")[0]
            if "```" in clean_completion
            else clean_completion
        )
        return clean_completion

    def get_system_prompt(self) -> str:
        """Returns the system prompt for the given run mode"""
        if self.run_mode == RunMode.VANILLA:
            raise ValueError("Vanilla mode does not have a system prompt")
        elif self.run_mode == RunMode.VANILLA_AGENT_RETURN_ONLY:
            return VANILLA_SYSTEM_PROMPT
        elif self.run_mode == RunMode.ADVANCED_AGENT_RETURN_ONLY:
            return ADVANCED_SYSTEM_PROMPT
        elif self.run_mode == RunMode.BAD_AGENT_RETURN_ONLY:
            return BAD_SYSTEM_PROMPT
        else:
            raise ValueError(f"Invalid run mode: {self.run_mode}")

    def get_formatted_instruction(self, raw_prompt: str) -> str:
        """Formats the instruction for the given prompt"""

        if self.run_mode == RunMode.VANILLA:
            return textwrap.dedent(
                """
            Below is an instruction that describes a task. 
            Write a response that appropriately completes the request.

            ### Instruction:
            Complete the following Python code: 
            Notes: respond with the entire complete function definition
            do not add any comments, be as concise in your code as possible
            use only built-in libraries, assume no additional imports other than those provided (if any)

            code:
            ```python
            {PROMPT}
            ```

            ### Response:
                        """
            ).format(PROMPT=raw_prompt)

        else:
            return textwrap.dedent(
                """                
            Below is an instruction that describes a task. Immediately return a result as a markdown snippet which solves this task to the user using the `call_termination` function.

            ### Instruction:
            Complete the following Python code: 
            Notes: respond with the entire complete function definition
            do not add any comments, be as concise in your code as possible
            use only built-in libraries, assume no additional imports other than those provided (if any).

            code:
            ```python
            {PROMPT}
            ```
            """
            ).format(PROMPT=raw_prompt)
