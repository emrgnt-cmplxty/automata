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
    DEFAULT_CONTEXT = "from typing import *\nfrom collections import *\n"

    def __init__(self):
        self.execution_context: List[
            str
        ] = PyInterpreter.DEFAULT_CONTEXT.split("\n")

    def __repr__(self) -> str:
        return f"PyInterpreter(execution_context={self.execution_context})"

    def _attempt_execution(self, code: str) -> Tuple[bool, str]:
        """Attempts to execute the provided code."""
        output_buffer = io.StringIO()
        try:
            return self._execute_code(
                "\n".join(self.execution_context) + "\n" + code, output_buffer
            )
        except Exception as e:
            error_message = str(e) or "Unknown error occurred."
            error_output = output_buffer.getvalue().strip()
            if error_output:
                error_message += f"\nOutput before error:\n{error_output}"
            return False, f"Execution failed with error = {error_message}"

    def _execute_code(
        self, code: str, output_buffer: io.StringIO
    ) -> Tuple[bool, str]:
        """Attempts to execute the provided code."""
        exec_payload = "try:\n" + "\n".join(
            [f"    {line}" for line in code.split("\n")]
        )
        exec_payload += "\nexcept AssertionError as ae:\n"
        exec_payload += "    global_exception = 'AssertionError on line ' + str(ae.__traceback__.tb_lineno) + ': ' + str(ae)\n"
        exec_payload += "    raise ValueError(f'An assertion error occurred on line {ae.__traceback__.tb_lineno}')"

        exec_payload += "\nexcept Exception as e:\n"
        exec_payload += "    global_exception = e\n"
        exec_payload += "    raise e"

        try:
            with contextlib.redirect_stdout(output_buffer):
                exec(exec_payload, {**globals()})
            execution_output = output_buffer.getvalue().strip()
            if execution_output:
                return (
                    True,
                    f"{PyInterpreter.SUCCESS_STRING}\nOutput:\n{execution_output}",
                )
            else:
                return True, PyInterpreter.SUCCESS_STRING
        except Exception as e:
            return (
                False,
                f"Execution failed with error '{e}' after outputting {output_buffer.getvalue().strip() or None}",
            )

    def set_code(self, code: str) -> str:
        """Sets up the provided code and persists the context to the local execution buffer."""
        code = self._clean_markdown(code)
        status, result = self._attempt_execution(code)
        if status:
            self.execution_context.extend(code.split("\n"))
        return result

    def run_tests(self, code: str) -> str:
        """Runs the provided test code, without affecting the persistent context."""
        code = self._clean_markdown(code)
        _, result = self._attempt_execution(code)
        return result

    def set_code_and_run_tests(self, code: str, test_code: str) -> str:
        """Sets up the provided code and then runs the provided test code."""
        set_code_result = self.set_code(code)
        run_tests_result = self.run_tests(test_code)
        return f"Set code result: {set_code_result}\nRun tests result: {run_tests_result}"

    def clear(self) -> None:
        """Clears the execution context."""
        self.execution_context = PyInterpreter.DEFAULT_CONTEXT.split("\n")

    @staticmethod
    def _clean_markdown(code: str) -> str:
        """Clean the markdown code to be executable."""
        if "```python" in code:
            code = code.split("```python")[1]
        return code.split("```")[0]


class PyInterpreterToolkitBuilder(AgentToolkitBuilder):
    """A builder for tools which provide an execution environment for the agent"""

    def __init__(self, *args, **kwargs) -> None:
        self.python_interpreter = PyInterpreter()

    def build(self) -> List[Tool]:
        """Builds the tools for the interpreter."""
        return [
            Tool(
                name="py-set-code",
                function=self.python_interpreter.set_code,
                description="Sets up the provided Python markdown snippet in the local environment. The code is executed and its context is persisted across interactions.",
            ),
            Tool(
                name="py-run-tests",
                function=self.python_interpreter.run_tests,
                description="Runs the provided Python markdown snippet in the local environment. The code is executed without affecting the persistent context. This tool is ideal for running tests.",
            ),
            Tool(
                name="py-set-code-and-run-tests",
                function=self.python_interpreter.set_code_and_run_tests,
                description="Sets up the provided Python markdown snippet and then runs the provided test code in the local environment. The setup code's context is persisted, but the test code does not affect the persistent context.",
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
                "description": "The given Python code to execute, formatted as a markdown snippet, e.g. ```python\\n[CODE]``` and with newlines separated by the double-escaped newline char '\\n'.",
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
