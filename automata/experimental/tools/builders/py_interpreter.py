"""This module contains the PyInterpreterToolkitBuilder class."""
import contextlib
import io
import logging
from typing import List

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

    def execute_code(self, code: str) -> str:
        """Attempts to execute the provided code."""
        output_buffer = io.StringIO()
        try:
            # Execute the code within the existing execution context
            code = self._clean_markdown(code)
            payload = "\n".join(self.execution_context) + "\n" + code
            with contextlib.redirect_stdout(output_buffer):
                exec(payload)
            execution_output = output_buffer.getvalue().strip()
            result = PyInterpreter.SUCCESS_STRING
            if execution_output:
                result += f"Output:\n{execution_output}"
            return result
        except Exception as e:
            return f"Execution failed with error = {e}"

    def persistent_execute(self, code: str) -> str:
        """
        Executes the provided code and persists the context to the local execution buffer.
        """
        result = self.execute_code(code)
        if result == PyInterpreter.SUCCESS_STRING:
            self.execution_context.extend(
                self._clean_markdown(code).split("\n")
            )
        return result

    def clear_and_persistent_execute(self, code: str) -> str:
        """
        Clears the execution context and executes the provided code.
        """
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
                name="append-and-execute-python-code",
                function=self.python_interpreter.persistent_execute,
                description="Attempts to execute the given Python markdown snippet and then persists the newly given state across executions if successful. E.g. a snippet which reads like '```python\nx=5```'. This is a very useful tool for development, note that the environment has all relevant dependencies pre-installed.",
            ),
            Tool(
                name="clear-and-execute-execute-python-code",
                function=self.python_interpreter.clear_and_persistent_execute,
                description="Clears the current execution context and then attempts to execute the given Python markdown snippet. The latest executed code will persist if successful",
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
                "description": "The given Python code to execute, with newlines separated by the newline char '\n'.",
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
