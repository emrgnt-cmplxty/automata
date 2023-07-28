from abc import abstractmethod
from typing import List, Optional, Tuple

from automata.eval.eval_base import Action, Eval, EvalResult
from automata.llm import FunctionCall
from automata.tools import ToolExecution


class ToolEvalResult(EvalResult):
    """An abstract class to represent the result of a tool eval."""

    def __init__(
        self,
        expected_action: Action,
        observed_action: Optional[Action],
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.expected_action = expected_action
        self.observed_action = observed_action


class ToolEval(Eval):
    """Abstract class for evaluating tools' performance."""

    def generate_eval_result(
        self,
        exec_input: FunctionCall,
        expected_output: Action,
        executor: ToolExecution,
        *args,
        **kwargs,
    ) -> EvalResult:
        """Generates an eval result for a given set of instructions and expected actions."""

        observed_result = executor.execute(exec_input)
        observed_action = self.extract_action((exec_input, observed_result))

        return self.to_tool_result(
            expected_action=expected_output,
            observed_action=observed_action,
        )

    @abstractmethod
    def extract_action(
        self, input_action_tuple: Tuple[FunctionCall, str]
    ) -> Action:
        """Extracts a list of action from the given message."""
        pass

    def _filter_actions(self, actions: List[Action]) -> List[Action]:
        """In the context of ToolEval, there's only one action to be expected.
        Therefore, there's no need to filter actions."""
        raise NotImplementedError

    @abstractmethod
    def to_tool_result(
        self, expected_action: Action, observed_action: Optional[Action]
    ) -> ToolEvalResult:
        """Converts the evaluation result to a ToolEvalResult."""
        pass
