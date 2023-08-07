"""This module contains the PyInterpreterToolkitBuilder class."""
import contextlib
import io
import logging
from typing import List, Tuple

# Import the entire symbol module so that we can properly patch convert_to_ast_object
from automata.agent import (
    AgentToolkitBuilder,
    AgentToolkitNames,
    OpenAIAgentToolkitBuilder,
)
from automata.config import LLMProvider
from automata.llm import OpenAITool
from automata.singletons.toolkit_registry import (
    OpenAIAutomataAgentToolkitRegistry,
)
from automata.tools.tool_base import Tool

logger = logging.getLogger(__name__)


class PyInterpreter:
    """This class provides an execution environment for the agent."""

    SUCCESS_STRING = "Execution successful."

    def __init__(self):
        self.execution_context: List[str] = []

    def __repr__(self) -> str:
        return f"PyInterpreter(execution_context={self.execution_context})"

    def _execute_code(
        self, code: str, output_buffer: io.StringIO
    ) -> Tuple[bool, str]:
        """Attempts to execute the provided code."""
        with contextlib.redirect_stdout(output_buffer):
            exec(code, {})
        execution_output = output_buffer.getvalue().strip()
        result = PyInterpreter.SUCCESS_STRING
        if execution_output:
            result += f"\nOutput:\n{execution_output}"
        return True, result

    def _attempt_execution(self, code: str) -> Tuple[bool, str]:
        """Attempts to execute the provided code."""
        output_buffer = io.StringIO()
        try:
            return self._execute_code(code, output_buffer)
        except Exception as e:
            print(f"EXECUTION EXCEPTION = {e}")
            error_message = str(e) or "Unknown error occurred"
            error_output = output_buffer.getvalue().strip()
            if error_output:
                error_message += f"\nOutput before error:\n{error_output}"
            return False, f"Execution failed with error = {error_message}"

    def persistent_execute(self, code: str) -> str:
        """Executes the provided code and persists the context to the local execution buffer."""
        code = self._clean_markdown(code)
        payload = "\n".join(self.execution_context) + "\n" + code
        status, result = self._attempt_execution(payload)
        if status:
            self.execution_context.extend(
                self._clean_markdown(code).split("\n")
            )
        return result

    def standalone_execute(self, code: str) -> str:
        """Executes the provided code, after executing code in the local execution buffer."""
        code = self._clean_markdown(code)
        payload = "\n".join(self.execution_context) + "\n" + code
        _, result = self._attempt_execution(payload)
        return result

    def clear_and_persistent_execute(self, code: str) -> str:
        """Clears the execution context and executes the provided code."""
        self.execution_context.clear()
        return self.persistent_execute(code)

    def clear(self) -> None:
        """Clears the execution context."""
        self.execution_context = []

    @staticmethod
    def _clean_markdown(code: str) -> str:
        """Clean the markdown code to be executable."""
        return code.replace("```python", "").replace("```", "")


class PyInterpreterToolkitBuilder(AgentToolkitBuilder):
    """A builder for tools which provide an execution environment for the agent"""

    def __init__(self, *args, **kwargs) -> None:
        self.python_interpreter = PyInterpreter()

    def build(self) -> List[Tool]:
        """Builds the tools for the interpreter."""
        return [
            Tool(
                name="py-execute-discard",
                function=self.python_interpreter.standalone_execute,
                description="Attempts to execute the given Python markdown snippet in the local environment. Snippets are expected to read like '```python\\nx=5```'. The final return result contains the output text from execution and/or any associated errors. This tool should typically be used for executing test runs.",
            ),
            Tool(
                name="py-execute-persist",
                function=self.python_interpreter.persistent_execute,
                description="Similar to standalone py-execute-discard, except if successful, the provided code snippet is persisted in the local execution environment across interactions.",
            ),
            Tool(
                name="py-clear-and-execute-persist",
                function=self.python_interpreter.clear_and_persistent_execute,
                description="Similar to py-execute-persist, except the local environment is permanently cleared before running py-execute-persist.",
            ),
        ]


@OpenAIAutomataAgentToolkitRegistry.register_tool_manager
class PyInterpreterOpenAIToolkitBuilder(
    PyInterpreterToolkitBuilder, OpenAIAgentToolkitBuilder
):
    TOOL_NAME = AgentToolkitNames.PY_INTERPRETER
    LLM_PROVIDER = LLMProvider.OPENAI

    def build_for_open_ai(self) -> List[OpenAITool]:
        """Builds the tools associated with the Python interpreter for the OpenAI API."""
        tools = super().build()

        # Predefined properties and required parameters
        properties = {
            "code": {
                "type": "string",
                "description": "The given Python code to execute, formatted as a markdown snippet, e.g. ```python\n[CODE]``` and with newlines separated by the newline char '\n'.",
            },
        }
        required = ["code"]

        return [
            OpenAITool(
                function=tool.function,
                name=tool.name,
                description=tool.description,
                properties=properties,
                required=required,
            )
            for tool in tools
        ]
