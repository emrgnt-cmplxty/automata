import textwrap

import pytest

from automata.experimental.tools import (
    PyInterpreter,
    PyInterpreterToolkitBuilder,
)
from automata.tools.tool_base import Tool


def test_python_interpreter_init():
    interpreter = PyInterpreter()
    assert isinstance(interpreter, PyInterpreter)
    assert (
        interpreter.execution_context
        == PyInterpreter.DEFAULT_CONTEXT.split("\n")
    )


def test_python_interpreter_execute_code():
    interpreter = PyInterpreter()
    assert (
        interpreter.standalone_execute("```python\nx = 5```")
        == PyInterpreter.SUCCESS_STRING
    )
    assert (
        interpreter.standalone_execute("```python\ny = x + 5```")
        == "Execution failed with error 'name 'x' is not defined' after outputting None"
    )


def test_python_interpreter_assertion():
    interpreter = PyInterpreter()
    assert (
        interpreter.standalone_execute("```python\nassert False```")
        == "Execution failed with error 'An assertion error occurred on line 6' after outputting None"
    )


def test_python_interpreter_persistent_execute():
    interpreter = PyInterpreter()
    assert (
        interpreter.persistent_execute("x = 5") == PyInterpreter.SUCCESS_STRING
    )
    assert (
        interpreter.persistent_execute("y = x + 5")
        == PyInterpreter.SUCCESS_STRING
    )
    assert (
        interpreter.persistent_execute("z = x + y + 5")
        == PyInterpreter.SUCCESS_STRING
    )
    assert (
        interpreter.persistent_execute("z == 20")
        == PyInterpreter.SUCCESS_STRING
    )
    assert interpreter.execution_context == interpreter.DEFAULT_CONTEXT.split(
        "\n"
    ) + [
        "x = 5",
        "y = x + 5",
        "z = x + y + 5",
        "z == 20",
    ]


def test_python_interpreter_import():
    interpreter = PyInterpreter()
    assert interpreter.persistent_execute("import random")
    assert interpreter.persistent_execute("import automata")


def test_python_interpreter_clear_and_persistent_execute():
    interpreter = PyInterpreter()
    interpreter.persistent_execute("x = 5")
    assert (
        interpreter.clear_and_persistent_execute("y = 10")
        == PyInterpreter.SUCCESS_STRING
    )
    assert (
        interpreter.execution_context
        == PyInterpreter.DEFAULT_CONTEXT.split("\n") + ["y = 10"]
    )


def test_python_interpreter_clear():
    interpreter = PyInterpreter()
    interpreter.persistent_execute("x = 5")
    interpreter.clear()
    assert (
        interpreter.execution_context
        == PyInterpreter.DEFAULT_CONTEXT.split("\n")
    )


def test_python_interpreter_toolkit_builder_init():
    builder = PyInterpreterToolkitBuilder()
    assert isinstance(builder.python_interpreter, PyInterpreter)


def test_python_interpreter_toolkit_builder_build():
    builder = PyInterpreterToolkitBuilder()
    tools = builder.build()
    assert len(tools) == 3
    for tool in tools:
        assert isinstance(tool, Tool)


@pytest.mark.parametrize(
    "tool_name, function_name, code, expected_result",
    [
        (
            "persistent-execute-python-code",
            "persistent_execute",
            "x = 5",
            PyInterpreter.SUCCESS_STRING,
        ),
        (
            "clear-and-execute-execute-python-code",
            "clear_and_persistent_execute",
            "y = 10",
            PyInterpreter.SUCCESS_STRING,
        ),
    ],
)
def test_python_interpreter_toolkit_builder_tool_functions(
    tool_name, function_name, code, expected_result
):
    builder = PyInterpreterToolkitBuilder()
    tools = builder.build()
    for tool in tools:
        if tool.name == tool_name:
            result = tool.function(code)
            assert result == expected_result


def test_build_py_writer():
    interpreter = PyInterpreter()

    result_0 = interpreter.persistent_execute(
        "```python\nfrom automata.code_parsers.py.py_reader import PyReader\n\nreader = PyReader()\n```"
    )

    assert result_0 == PyInterpreter.SUCCESS_STRING
    result_1 = interpreter.persistent_execute(
        "```python\nfrom automata.code_writers.py.py_code_writer import PyCodeWriter\n\nx = PyCodeWriter(reader)\n```"
    )

    assert result_1 == PyInterpreter.SUCCESS_STRING


example_text = textwrap.dedent(
    """
```python
import heapq

class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

class Solution:
    def mergeKLists(self, lists):
        dummy = ListNode(None)
        curr = dummy
        h = []
        for i in range(len(lists)):
            if lists[i] is not None:
                h.append((lists[i].val, i))
                lists[i] = lists[i].next
        heapq.heapify(h)
        while h:
            val, i = heapq.heappop(h)
            curr.next = ListNode(val)
            curr = curr.next
            if lists[i] is not None:
                heapq.heappush(h, (lists[i].val, i))
                lists[i] = lists[i].next
        return dummy.next

# function to convert list to linked list

def listToLinkedList(lst):
    dummy = ListNode(0)
    ptr = dummy
    for i in lst:
        ptr.next = ListNode(i)
        ptr = ptr.next
    return dummy.next

# function to convert linked list to list
def linkedListToList(node):
    res = []
    while node:
        res.append(node.val)
        node = node.next
    return res
```
"""
)


def test_python_interpreter_execute_code_advanced():
    interpreter = PyInterpreter()
    assert (
        interpreter.persistent_execute(example_text)
        == PyInterpreter.SUCCESS_STRING
    )


example_text_2 = textwrap.dedent(
    """
import heapq

# Define the structure for the linked list node.
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

# Main function to solve the problem
def mergeKLists(lists):
    # Custom comparison for heap elements
    ListNode.__lt__ = lambda x, y : x.val < y.val
    
    # Initialize min heap and fill it
    preprocess = [i for i in lists if i]
    heapq.heapify(preprocess)

    # Use dummy head technique to easily return the result
    dummyHead = node = ListNode(0)

    while preprocess:
        temp = heapq.heappop(preprocess)
        if temp.next:
            heapq.heappush(preprocess, temp.next)
        node.next = temp
        node = node.next

    return dummyHead.next
"""
)


def test_python_interpreter_execute_code_advanced_2():
    interpreter = PyInterpreter()
    assert (
        interpreter.persistent_execute(example_text_2)
        == PyInterpreter.SUCCESS_STRING
    )


example_text_3 = "```python\nimport heapq\n\ndef smallestRange(nums):\n    minHeap = []\n    maxVal = -1e9\n    \n    for i, lst in enumerate(nums):\n        heapq.heappush(minHeap, (lst[0], i))\n        maxVal = max(maxVal, lst[0])\n        \n    listIndices = [0] * len(nums)\n    minRange = 1e9\n    start, end = -1, -1\n    \n    while len(minHeap) == len(nums):\n        val, listIdx = heapq.heappop(minHeap)\n        range_ = maxVal - val\n        \n        if range_ < minRange:\n            minRange = range_\n            start, end = val, maxVal\n            \n        listIndices[listIdx] += 1\n        if listIndices[listIdx] < len(nums[listIdx]):\n            newVal = nums[listIdx][listIndices[listIdx]]\n            heapq.heappush(minHeap, (newVal, listIdx))\n            maxVal = max(maxVal, newVal)\n            \n    return [start, end]\n\nprint(smallestRange([[4,10,15,24,26],[0,9,12,20],[5,18,22,30]]))\nprint(smallestRange([[1,2,3],[1,2,3],[1,2,3]]))\n```"


def test_python_interpreter_execute_code_advanced_3():
    interpreter = PyInterpreter()
    result = interpreter.persistent_execute(example_text_3)
    assert (
        result == f"{PyInterpreter.SUCCESS_STRING}\nOutput:\n[20, 24]\n[1, 1]"
    )


def test_python_interpreter_execute_code_advanced_4():
    example_text_4 = """```python\\nfrom typing import List\\n\\nclass Solution:\\n    def minReverseOperations(self, n: int, p: int, banned: List[int], k: int) -> List[int]:\\n        # Initialize the array with 0's, except at position p\\n        arr = [0 for _ in range(n)]\\n        arr[p] = 1\\n\\n        # Apply the banned positions\\n        for pos in banned:\\n            arr[pos] = 0\\n\\n        # Initialize the result array with -1's\\n        ans = [-1 for _ in range(n)]\\n\\n        # For each position, we check if we can move the 1 there\\n        for i in range(0, n):\\n            if i == p:  # No operations needed\\n                ans[i] = 0\\n                continue\\n\\n            # Using sliding window approach and two pointers\\n            j = max(0, i - k + 1)  # Start of the window\\n            while j + k - 1 < n:  # Until the window goes out of the array\\n                valid = True\\n                for banned_pos in banned:\\n                    if banned_pos >= j and banned_pos < j + k:  # If a banned position is in the window\\n                        valid = False\\n                        break\\n\\n                if valid and abs(p - i) % k == 0:  # If we can move the 1 inside the window\\n                    op_count = abs(p - i) // k\\n                    if ans[i] == -1 or ans[i] > op_count:  # We're looking for the minimum operation count\\n                        ans[i] = op_count\\n\\n                j += 1  # Slide the window\\n\\n        return ans\\n```"""

    example_text_4 = """```python
from typing import List

class Solution:
    def minReverseOperations(self, n: int, p: int, banned: List[int], k: int) -> List[int]:
        return n
    
```"""

    interpreter = PyInterpreter()
    result = interpreter.persistent_execute(example_text_4)
    result == PyInterpreter.SUCCESS_STRING
