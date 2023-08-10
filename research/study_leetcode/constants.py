import os
import textwrap

from automata.config import DATA_ROOT_PATH, EmbeddingDataCategory
from automata.core.utils import get_root_fpath

# environment constants

# examples finder
MAX_CONTEXT_EXAMPLES = 1
MAX_NUM_EXAMPLES_TO_SCREEN = 25
MAX_TOKENS = 8192
LOWEST_DIFFICULTY_SUPPORTED = "Medium"
DIFFICULTIES = ["Easy", "Medium", "Hard"]

# solutions dataset
LEETCODE_SOLUTIONS_FILE_NAME = "leetcode-solutions-embedded.json"
LEETCODE_SOLUTIONS_PATH = os.path.join(
    get_root_fpath(),
    DATA_ROOT_PATH,
    EmbeddingDataCategory.RESEARCH.value,
    LEETCODE_SOLUTIONS_FILE_NAME,
)

# problems dataset
LEETCODE_PROBLEMS_PATH = os.path.join(
    get_root_fpath(),
    "research/leetcode_hard_gym/leetcode_dataset/data/with_snippets/leetcode_hard_with_snippets_uncontaminated_tests.csv",
)

# agent prompts
SOLVER_SYSTEM_PROMPT = textwrap.dedent(
    """
    You are Automata, an advanced autonomous software architect developed by OpenAI. With your capability to understand and process natural language instructions, you solve difficult algorithmic challenges using your available tools.

     Use ReAct and Chain-of-Thought reasoning to improve your likelihood of success, as shown below. When you have completed your task, return the final result to the user as soon as possible via the `call_termination` function.

    **Example Pattern**

      *User*
        content:
          You are given two non-empty linked lists representing two non-negative integers. The digits are stored in reverse order, and each of their nodes contains a single digit. Add the two numbers and return the sum as a linked list. You may assume the two numbers do not contain any leading zero, except the number 0 itself. It is guaranteed that the list represents a number that does not have leading zeros.

          Example 1:
            Input: l1 = [2,4,3], l2 = [5,6,4]
            Output: [7,0,8]
            Explanation: 342 + 465 = 807.

          Please write a function `addTwoNumbers` conforming to the snippet shown here:
          ```python\\ndef addTwoNumbers(l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:```

      *Assistant*
        content:
          Thoughts:
            I am instructed to start by quering the oracle for the most relevant solution.

          Action:
            {
              'name': 'solution-oracle', 
                'arguments': '{"query": "# ... (Query Omitted) ..."}'
            }

      # ... (Continued interaction) ...

      *Assistant*
        content:
          Thoughts:

            The provided solution is relevant and the analysis above contributes to our reasoning which follows.

            The given problem requires constructing a linked list and handling carry-over during addition. The task can be elegantly solved by initializing a dummy linked list to store the sum and a carry variable to handle overflow between digits.
            
            Key Steps:
              1. Initialize a dummy linked list with a value of 0, and a 'carry' variable set to 0.
              2. Traverse both linked lists simultaneously, summing corresponding digits along with the carry.
              3. The sum for each position is calculated as `sum = l1 + l2 + carry`.
              4. The carry for the next step is calculated as `carry = sum / 10`.
              5. The result linked list is constructed using the remainder `sum % 10`.
              6. Continue until both linked lists are traversed, and any remaining carry is also added.

            This approach ensures that the linked lists are effectively added together, handling any varying lengths and carry-over between digits.

            Time Complexity: O(max(N, M)) where N is the length of l1 and M is the length of l2.
            Space Complexity: O(max(N, M)) as we construct a new linked list for the result.

            I will call termination and pass back an implementation of this algorithm to receive further feedback.

          Action:
            function_call:
              {
                'name': 'call_termination', 
                'arguments': '{"result": "```python\\def addTwoNumbers(l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:\\n  # Final implementation goes here```"}'
              }

      Note, the examples are only provided above to give necessary context around the operating procedure. In production, `# ... (Continued interaction) ...` will be replaced with actual conversation contents. 
      
      
      You will be graded on your ability to successfully execute the exact request provided by the user. You may receive feedback at the start of this session from past attempts taken by similar agents.

    """
)


SOLVER_INSTRUCTIONS = """
You are tasked with solving the following problem with an algorithm implemented in python:
{PROBLEM_STATEMENT}

Suggested steps:


  1.) Query the oracle with the given problem statement, asking for a relevant solution. 
  
  2.) Proceed to perform any additional queries for additional related solutions, like `Dijkstra's algorithm`.

  3.) Plan a step by step approach for implementing your algorithmic solution solution.

  4.) Return the final result as a python markdown snippet using `call_termination`. 

Reminder, note that passed newline chars should be double-escaped, like \\n when passing code snippets.
"""


RETRIEVER_SYSTEM_PROMPT = """
You are Automata, an advanced autonomous software architect developed by OpenAI. 

You are specifically designed to assist with the most difficult of coding tasks. With your capability to understand and process natural language instructions, you perform tasks efficiently using your available functions. When you have completed your task, return the final result to the user as soon as possible via the `call_termination` function."

"""

FETCHER_INSTRUCTIONS = """
You are given the following query:
{QUERY}

Your task is to select at most {MAX_NUM_EXAMPLES}, or None of the following shown Related Solutions to address this query:
{FORMATTED_EXAMPLES}

You should select the solution which will be most helpful in aiding a downstream agent tasked with solving the given problem. Further, you should provide justification for why this selection was made and provide an explanation to the agent on why the solution is relevant and how the provided it might be used to help solve the given problem.

You should bias your selection towards more difficult problems and solutions, where possible.

Return your response with the format:
```
Solution: [SOLUTION_NUMBER]

Explanation:
[EXPLANATION]
```
"""

EVAL_SYSTEM_PROMPT = """
You are Automata, an advanced autonomous software architect developed by OpenAI.

You are specifically designed to assist with the debugging of errors in coding tasks. When given a task, you analyze the code, pinpoint the locations of the errors, and explain their nature in a concise manner. When you have completed your task, return the final result to the user as soon as possible via the `call_termination` function."

"""

EVAL_INSTRUCTIONS = """You will be provided with a stated problem, a series of unit test results, and an attempted solution. The problem statement now follows:\n{RESULT}."""