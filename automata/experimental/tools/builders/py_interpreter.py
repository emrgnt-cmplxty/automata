"""This module contains the PyInterpreterToolkitBuilder class."""
import ast
import contextlib
import io
import logging
from typing import List, Optional, Tuple

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
    DEFAULT_CODE_CONTEXT = "from typing import *\nfrom collections import *\n"
    DEFAULT_TEST_CONTEXT = ""

    def __init__(self):
        self.code_context: List[
            str
        ] = PyInterpreter.DEFAULT_CODE_CONTEXT.split("\n")

        self.test_context: List[
            str
        ] = PyInterpreter.DEFAULT_TEST_CONTEXT.split("\n")

    def __repr__(self) -> str:
        return f"PyInterpreter(code_context={self.code_context}, test_context={self.test_context})"

    def _attempt_execution(self, code: str) -> Tuple[bool, str]:
        """Attempts to execute the provided code."""
        output_buffer = io.StringIO()
        try:
            return self._execute_code(
                "\n".join(self.code_context) + "\n" + code, output_buffer
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

    def set_tests(self, code: str, overwrite: bool = True) -> str:
        """Sets up the provided code and persists the context to the local execution buffer."""
        # Add extra handling for string input
        if isinstance(overwrite, str):
            overwrite = overwrite.lower() == "true"
        if overwrite:
            self.test_context = []
        code = self._clean_markdown(code)
        try:
            result: Optional[str] = None
            ast.parse(code)
            if self.code_context != PyInterpreter.DEFAULT_CODE_CONTEXT.split(
                "\n"
            ):
                code = "\n".join(self.code_context) + "\n" + code
                status, result = self._attempt_execution(code)
                if not status:
                    return result
            self.test_context.extend(code.split("\n"))
            return (
                f"{PyInterpreter.SUCCESS_STRING}\nresult = {result}"
                if result is not None
                else PyInterpreter.SUCCESS_STRING
            )
        except Exception as e:
            return f"Execution failed with error '{e}'."

    def set_code(self, code: str, overwrite: bool = True) -> Tuple[bool, str]:
        """Sets up the provided code and persists the context to the local execution buffer."""
        # Add extra handling for string input
        if isinstance(overwrite, str):
            overwrite = overwrite.lower() == "true"
        if overwrite:
            self.code_context = [
                str(ele)
                for ele in PyInterpreter.DEFAULT_CODE_CONTEXT.split("\n")
            ]

        code = self._clean_markdown(code)
        status, result = self._attempt_execution(code)
        if status:
            self.code_context.extend(code.split("\n"))
        return status, result

    def set_code_and_run_tests(self, code: str, overwrite: bool = True) -> str:
        """Set the code and then run the local tests"""
        status, result = self.set_code(code, overwrite)
        result = f"Code Exec Result:\n{result}"
        if status:
            result += "\n" + f"Test Exec Result:\n{self._run_tests()}"
        return result

    def _run_tests(self) -> str:
        """Runs the internal test code."""
        code = "\n".join(self.test_context)
        _, result = self._attempt_execution(code)
        return result

    @staticmethod
    def _clean_markdown(code: str) -> str:
        """Clean the markdown code to be executable."""
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
                name="py-set-tests",
                function=self.py_interpreter.set_tests,
                description="Sets up the provided Python markdown snippet in the test environment. The code is parsed and persisted across interactions. If `overwrite` is set to true then existing test code is overwritten. The user should note that using assertions in tests results in poor error reporting due to the code environment, for this reason it is better to raise exceptions directly.",
            ),
            Tool(
                name="py-set-code-and-run-tests",
                function=self.py_interpreter.set_code_and_run_tests,
                description="Sets up the provided Python markdown snippet in the local source environment. The code is executed and its context is persisted in the source environment across interactions. After successfully executing the provided code, the provided tests are then ran. If `overwrite` is set to true then existing source code environment is overwritten (but not the tests).",
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
                "description": "The given Python code to execute, formatted as a markdown snippet, e.g. ```python\\n[CODE]``` and with newlines separated by the double-escaped newline char '\\n'. When providing tests, favor raising exceptions directly to asserting.",
            },
            "overwrite": {
                "type": "string",
                "description": "Specifies whether or not the given code should overwrite the existing code in the interpreter.",
                "default": "True",
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
