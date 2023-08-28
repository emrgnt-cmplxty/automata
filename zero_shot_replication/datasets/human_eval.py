import textwrap
from typing import Any, Generator, List, Tuple

from evalplus.data import get_human_eval_plus

from zero_shot_replication.core import BaseDataset
from zero_shot_replication.model.base import PromptMode


class HumanEvalDataset(BaseDataset):
    """A concrete class to provide HumanEval problems for the runner."""

    HUMAN_EVAL_TEMPLATE = textwrap.dedent(
        """
    ### Instruction:
    Provide a response which completes the following Python code:

    ```python
    {CODE_PROMPT}
    ```

    ### Notes:
    Respond with the entire complete function definition, including a re-stated function definition.
    Use only built-in libraries and numpy, assume no additional imports other than those provided in the problem statement.
    Do not add any comments, be as concise in your code as possible.
    """
    )
    HUMAN_EVAL_TEMPLATE_COMPLETION = textwrap.dedent(
        """
    {CODE_PROMPT}
    """
    )

    @property
    def raw_prompt(self) -> str:
        """Concrete property to get the raw prompt for a HumanEval problem."""
        return HumanEvalDataset.HUMAN_EVAL_TEMPLATE

    @property
    def raw_completion_prompt(self) -> str:
        """Concrete property to get the raw completion prompt for a HumanEval problem."""
        return HumanEvalDataset.HUMAN_EVAL_TEMPLATE_COMPLETION

    @property
    def input_paths(self) -> List[str]:
        """Concrete method to get a list over the HumanEval dataset paths."""
        raise NotImplementedError(
            "HumanEvalDataset does not have input paths."
        )

    @property
    def generator(self) -> Generator[Tuple[str, Any], None, None]:
        """Concrete method to get a generator over the HumanEval problems."""

        #  Fields on the yielded problem are ['task_id', 'prompt', 'entry_point',
        # 'canonical_solution', 'test', 'contract', 'base_input', 'atol', 'plus_input']
        yield from get_human_eval_plus().items()

    def get_formatted_prompt(
        self,
        problem: dict,
        prompt_mode: PromptMode = PromptMode.HUMAN_FEEDBACK,
    ) -> str:
        """Concrete method to get the formatted prompt for HumanEval problems."""
        match prompt_mode:
            case PromptMode.HUMAN_FEEDBACK:
                return self.raw_completion_prompt.format(
                    CODE_PROMPT=problem["prompt"]
                )
            case PromptMode.COMPLETION:
                return self.raw_prompt.format(CODE_PROMPT=problem["prompt"])
            case _:
                raise ValueError("Invalid prompt mode.")
