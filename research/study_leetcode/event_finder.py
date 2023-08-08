# sourcery skip: avoid-global-variables
import os

import pandas as pd

from automata.core.utils import get_root_fpath

DATA_PATH = "research/leetcode-hard-gym/leetcode_dataset/data/with_snippets/leetcode_hard_with_snippets_uncontaminated_cleaned_tests.csv"


class LeetCodeLoader:
    """Concrete class responsible for loading and providing LeetCode problems."""

    def __init__(self, data_path):
        self.data_path = data_path
        self.data = pd.read_csv(self.data_path)

    def get_problem(self, idx):
        """Retrieve a problem by its index."""
        row = self.data.iloc[idx]
        return f"{row['title']}:\n{row['description']}\n\nNote, your final solution MUST conform to the snippet shown here - {row['python3_code_snippet']}"


if __name__ == "__main__":
    raw_data = pd.read_csv(os.path.join(get_root_fpath(), DATA_PATH))
    raw_data_selected = raw_data[
        raw_data.question_slug == "minimum-reverse-operations"
    ]

    lang = "python3"
    question_id = raw_data_selected["question_id"]
    question_slug = raw_data_selected["question_slug"]
    question_title = raw_data_selected["question_title"]
    description = raw_data_selected["description"]
    python3_snippet = raw_data_selected["python3_snippet"]

    print("question_id: ", question_id.values[0])
    print("question_slug: ", question_slug.values[0])
    print("question_title: ", question_title.values[0])
    print("description: ", description.values[0])
    print("python3_snippet: ", python3_snippet.values[0])
