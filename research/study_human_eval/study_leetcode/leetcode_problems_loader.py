import textwrap
from typing import Any, Tuple

import pandas as pd

"""An implementation for loading leetcode problems from the gym"""


class LeetCodeLoader:
    """Concrete class responsible for loading and providing LeetCode problems."""

    def __init__(self, data_path: str):
        self.data_path = data_path
        self.data = pd.read_csv(self.data_path)

    def get_problem_header(self, idx: int) -> str:
        """Retrieve a problem by its index."""
        row = self.data.iloc[idx]
        return f"Title:{row['question_title']}\n\nDescription:\n{row['description']}"

    def get_problem_context(self, idx: int) -> str:
        """Retrieve a problem by its index."""
        row = self.data.iloc[idx]
        description = row["description"]
        # We remove constraints since they are improperly formatted
        description_ex_constraints = description.split("Constraints:")[
            0
        ].strip()

        snippet_text = (
            row["python3_snippet"]
            .replace("class Solution:\n", "")
            .replace("self, ", "")
            .strip()
        )
        cleaned_snippet = textwrap.dedent(snippet_text)  # type: ignore

        return f"Title:{row['question_title']}\n\nDescription:\n{description_ex_constraints}\n\nNote, your final solution MUST BEGIN WITH the snippet shown here - ```python\\n{cleaned_snippet}```"

    def get_problem_id_slug(self, idx: int) -> Tuple[int, int, Any]:
        """Retrieve a problem by its index."""
        row = self.data.iloc[idx]
        return (
            int(row["frontend_question_id"]),  # type: ignore
            int(row["question_id"]),  # type: ignore
            row["question_slug"],
        )

    def get_problem_slug(self, idx: int) -> Any:
        """Get the backend problem id for a given problem."""
        row = self.data.iloc[idx]
        return str(row["question_slug"])  # type: ignore

    def get_backend_problem_id(self, idx: int) -> int:
        """Get the backend problem id for a given problem."""
        row = self.data.iloc[idx]
        return int(row["question_id"])  # type: ignore

    def get_frontend_problem_id(self, idx: int) -> int:
        """Get the frontend problem id for a given problem."""
        row = self.data.iloc[idx]
        return int(row["frontend_question_id"])  # type: ignore
