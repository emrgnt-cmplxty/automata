# sourcery skip: avoid-single-character-names-variables, docstrings-for-classes, docstrings-for-modules
import ast
import collections
import inspect
from typing import Any, Dict, List, Optional, Tuple

from leetcode_problems_loader import LeetCodeLoader


class TreeNode:
    def __init__(
        self,
        val: int = 0,
        left: Optional["TreeNode"] = None,
        right: Optional["TreeNode"] = None,
    ):
        self.val = val
        self.left = left
        self.right = right


def array_to_binary_tree(arr: List[Optional[int]]) -> Optional[TreeNode]:
    """Converts an array to a binary tree with the given values."""
    if not arr or arr[0] is None:
        return None

    root = TreeNode(arr[0])
    queue = collections.deque([root])
    i = 1

    while queue and i < len(arr):
        node = queue.popleft()

        if arr[i] is not None:
            node.left = TreeNode(arr[i])  # type: ignore
            queue.append(node.left)
        i += 1

        if i < len(arr) and arr[i] is not None:
            node.right = TreeNode(arr[i])  # type: ignore
            queue.append(node.right)
        i += 1

    return root


class LeetCodeTestStand:
    def __init__(self, loader: LeetCodeLoader):
        self.loader = loader

    @staticmethod
    def convert_value(value: str, annotation: Any) -> Any:
        """Converts a string value to the given annotation type."""

        # Conversion logic for various types
        if annotation == int:
            return int(value)
        elif annotation == float:
            return float(value)
        elif annotation == bool:
            return value.lower() == "true"
        elif annotation == str:
            return value
        elif annotation == List[List[int]]:
            return [[int(x) for x in y] for y in eval(value)]
        elif annotation == List[int]:
            return [int(x) for x in eval(value)]
        elif annotation == Dict[str, int]:
            return {str(k): int(v) for k, v in eval(value).items()}
        elif annotation == List[str]:
            return [str(x) for x in eval(value)]
        elif annotation == Dict[str, str]:
            return {str(k): str(v) for k, v in eval(value).items()}
        elif annotation == Optional[TreeNode]:
            return array_to_binary_tree(
                [
                    int(x) if x != None else None
                    for x in eval(value.replace("null", "None"))
                ]
            )

        # Add more conversion logic for other types as needed
        else:
            raise ValueError(f"Unsupported annotation {annotation}...")

    def _run_tests(self, function: Any, test_cases: list) -> str:
        """Runs the test cases on the given function."""

        final_result = ""
        # Run test cases on the given function

        # Get the signature of the function
        signature = inspect.signature(function)
        parameters = list(signature.parameters.values())

        # Iterate through the test cases
        for test_case, expected_output in test_cases:
            args = []
            for param, value in zip(parameters, test_case.values()):
                # Convert the value based on the annotation in the function signature
                converted_value = self.convert_value(value, param.annotation)
                if (
                    isinstance(converted_value, str)
                    and "[" in converted_value
                    and "]" in converted_value
                ):
                    # Handle list conversion
                    converted_value = eval(converted_value)
                args.append(converted_value)

            # Call the function with the converted arguments
            exec_result = function(*args)

            # Compare the result with the expected output
            expected_output = self.convert_value(
                expected_output, signature.return_annotation
            )
            if exec_result == expected_output:
                final_result += f"Test passed for {test_case}.\n"
            else:
                final_result += f"Test failed for {test_case}, expected {expected_output}, but found {exec_result}.\n"

        return final_result

    def run_test_for_example(
        self,
        example_index: int,
        function_string: str,
    ) -> Tuple[Optional[str], Optional[str]]:
        """Runs the test for a specific example using the given function string."""

        # Extract the function from the string
        local_scope = {}
        try:
            exec(function_string, globals(), local_scope)
        except Exception as e:
            return str(e), None

        function_obj = next(
            (obj for obj in local_scope.values() if inspect.isfunction(obj)),
            None,
        )
        if not function_obj:
            return "No function found in the given string.", None
        # Run tests for the specific example
        try:
            test_cases = ast.literal_eval(
                self.loader.data.iloc[example_index]["example_test_cases"]
            )
            result = self._run_tests(function_obj, test_cases)
            return None, result
        except Exception as e:
            return str(e), None
