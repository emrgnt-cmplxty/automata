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
        return f"Title:{row['question_title']}\n\nDescription:\n{row['description']}\n\nNote, your final solution MUST conform to the snippet shown here - ```python\\n{row['python3_snippet']}```"

    def get_problem_id_slug(self, idx: int) -> Tuple[int, int, Any]:
        """Retrieve a problem by its index."""
        row = self.data.iloc[idx]
        return (
            int(row["frontend_question_id"]),
            int(row["question_id"]),
            row["question_slug"],
        )
