"""This module contains the PyInterpreterToolkitBuilder class."""
import ast
import contextlib
import io
import logging
import logging.config
import signal
from typing import List, Optional, Tuple

# Import the entire symbol module so that we can properly patch convert_to_ast_object
from automata.agent import (
    AgentToolkitBuilder,
    AgentToolkitNames,
    OpenAIAgentToolkitBuilder,
)
from automata.core.utils import get_logging_config
from automata.llm import OpenAITool
from automata.singletons.toolkit_registry import (
    OpenAIAutomataAgentToolkitRegistry,
)
from automata.tools.tool_base import Tool

logger = logging.getLogger(__name__)
logging.config.dictConfig(get_logging_config())


class PyInterpreter:
    """This class provides an execution environment for the agent."""

    SUCCESS_STRING = "Execution successful."
    DEFAULT_CODE_CONTEXT = "from typing import *\nfrom collections import *\nimport numpy as np\nimport sympy as sp\n"

    def __init__(self):
        self.source_code = ""
        self.test_code = ""

    def __repr__(self) -> str:
        return f"PyInterpreter(source_code={self.source_code}, test_code={self.test_code})"

    def _attempt_execution(self, provided_code: str) -> Tuple[bool, str]:
        """Attempts to execute the provided code."""
        output_buffer = io.StringIO()
        try:
            return self._execute_code(
                PyInterpreter.DEFAULT_CODE_CONTEXT + "\n" + provided_code,
                output_buffer,
            )
        except Exception as e:
            error_message = str(e) or "Unknown error occurred."
            if error_output := output_buffer.getvalue().strip():
                error_message += f"\nOutput before error:\n{error_output}"
            return False, f"Execution failed with error = {error_message}"

    def _execute_code(
        self, code: str, output_buffer: io.StringIO
    ) -> Tuple[bool, str]:
        """Attempts to execute the provided code."""
        exec_payload = "try:\n" + "\n".join(
            [f"    {line}" for line in code.split("\n") + ["pass"]]
        )
        exec_payload += "\nexcept AssertionError as ae:\n"
        exec_payload += "    global_exception = 'AssertionError on line ' + str(ae.__traceback__.tb_lineno) + ': ' + str(ae)\n"
        exec_payload += "    raise ValueError(f'An assertion error occurred on line {ae.__traceback__.tb_lineno}')"

        exec_payload += "\nexcept Exception as e:\n"
        exec_payload += "    global_exception = e\n"
        exec_payload += "    raise e"

        def handler(signum, frame) -> TimeoutError:
            raise TimeoutError("Execution timed out")

        signal.signal(signal.SIGALRM, handler)
        # TODO - move to decorator to enable cross-platform compatibility
        # external dependency `timeout_decorator` is one potential choice

        signal.alarm(5)  # Set a 5-second alarm

        try:
            with contextlib.redirect_stdout(output_buffer):
                exec(exec_payload, {**globals()})
            if execution_output := output_buffer.getvalue().strip():
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
        finally:
            signal.alarm(0)  # Disable the alarm

    def _update_env(
        self,
        source_code: Optional[str] = None,
        test_code: Optional[str] = None,
    ) -> str:
        """Updates the environment with the provided code."""
        if source_code:
            self.source_code = self._extract_code(source_code)
        if test_code:
            self.test_code = self._extract_code(test_code)

        exec_result, source_result = self._attempt_execution(self.source_code)
        if not exec_result:
            return f"Source code execution failed with {source_result}."

        exec_result, test_result = self._attempt_execution(
            f"{self.source_code}\n{self.test_code}"
        )
        if not exec_result:
            return f"Test code execution failed with {test_result}."

        return PyInterpreter.SUCCESS_STRING

    @staticmethod
    def _extract_code(code: str) -> str:
        """Extracts the cleaned markdown code to be executable."""
        if "```python" in code:
            code = code.split("```python")[1]
        return code.split("```")[0]


class PyInterpreterToolkitBuilder(AgentToolkitBuilder):
    """A builder for tools which provide an execution environment for the agent"""

    def __init__(self, *args, **kwargs) -> None:
        self.py_interpreter = PyInterpreter()

    def build(self) -> List[Tool]:
        """Builds the tools for the interpreter."""
        return [
            Tool(
                name="py-update-and-run-env",
                function=self.py_interpreter._update_env,
                description="""
                Extracts code from the provided as Python markdown snippets into the source and test code environment. Provided code is persisted across sessions, and when new code is not provided the existing context is used. The user must call `print(...)` on any output they would like to see returned from the environment and the user will include this in their next message. For instance, if your execution concludes with a variable `x`, then to see the result you should terminate with `print(x)`.
                """,
            ),
        ]


@OpenAIAutomataAgentToolkitRegistry.register_tool_manager
class PyInterpreterOpenAIToolkitBuilder(
    PyInterpreterToolkitBuilder, OpenAIAgentToolkitBuilder
):
    TOOL_NAME = AgentToolkitNames.PY_INTERPRETER

    def build_for_open_ai(self) -> List[OpenAITool]:
        """Builds the tools associated with the Python interpreter for the OpenAI API."""
        tools = super().build()

        # Predefined properties and required parameters
        properties = {
            "source_code": {
                "type": "string",
                "description": "The given source code, formatted as a markdown snippet, e.g. ```python\\n[CODE]``` and with newlines separated by the double-escaped newline char '\\n'.",
            },
            "test_code": {
                "type": "string",
                "description": "The given test code, formatted as a markdown snippet, e.g. ```python\\n[CODE]``` and with newlines separated by the double-escaped newline char '\\n'. NOTE, DO NOT re-supply tests unless you would like to alter those passed previously.",
            },
        }
        required = []

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
