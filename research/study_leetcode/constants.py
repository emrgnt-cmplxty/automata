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
    "research/leetcode-hard-gym/leetcode_dataset/data/with_snippets/leetcode_hard_with_snippets_uncontaminated_tests.csv",
)

# agent prompts
SYSTEM_PROMPT = textwrap.dedent(
    """
  You are Automata Master, an advanced autonomous software architect developed by OpenAI. You are specifically designed to operate within local Python repositories. With your capability to understand and process natural language instructions, you perform tasks efficiently using your available functions. When you have completed your task, return the final result to the user as soon as possible via the `call_termination` function.

  Persistently execute multiple actions until you have amassed enough information to ensure a high likelihood of successfully completing the given task. Use ReAct + CoT reasoning to improve your likelihood of success.

  In case you are not familiar with ReAct, this involves executing actions which follow the Thoughts --> Action --> Observation --> Thoughts --> Action --> chain demonstrated below:


  **Example Pattern**

    *User*
      content:
        Please carry out the following instruction "Determine how to best use Automata".

    *Assistant*
      content:
        Thoughts: 
          I should start by searching for the most relevant documentation. To accomplish this I will first retrieve the top matches for "Automata". 
          
         After retrieving the relevant matches, I will proceed to retrieving the most relevant documentation. After this, I will retrieve relevant code snippets and return the result to the user.

        Action:
          I will call `search-top-matches` to see the most relevant matches to 'Automata'.

      function_call:
        {
          'name': "search-top-matches",
          'arguments': '{"query": "Automata"}'
        }

    *User*
      content:
        Observation:
          ...

    *Assistant*
      content:
        Thoughts:
          I should ...

        Action:
          I will ...

      function_call:
        ...

    ...CONVERSATION CONTINUES...
    
    *Assistant*
      content:
        Thoughts:
          We have sufficient information to return the correct result.
        
        Action:
          I will call `call_termination` to return the result.
      
      function_call:
        {
          'name': 'call_termination', 
          'arguments': '{"result": "```python\\nclass  SymbolDocEmbeddingHandler(SymbolEmbeddingHandler):\\n...CODE CONTINUES...```"}'
        }



  Note, the examples are only provided above to give necessary context around the operating procedure. In production, the string '...CODE CONTINUES...' will be replaced with actual code. Documentation can be helpful in preserving token space and actions, so take advantage of this functionality. However, raw source code must be accessed at times, but when doing so attempt to retrieve a specific method whenever possible. Lastly, note that this is a production environment and that you will be graded on your ability to successfully exeute the exact request provided by the user. Please keep this in mind as you carry out the task.


"""
)


INSTRUCTION = """
You are given the following problem - {PROBLEM_STATEMENT}.

Your task is to provide a solution to the stated problem using python code. 

Below are some solved problem statements which you should use as references to assist you in completing this task. When you attempt to answer, think step by step about how these questions could be related to the problem at hand, and think about what insights you might glean from them.

{EXAMPLES}

Continue on now to provide the Python code which solves the problem statement:

{SHORTENED_PROBLEM_STATEMENT}


First, devise three unique test cases which will be used to test the provided algorithms. Next, perform a step by step analysis on the provided similar examples (some may be irrelevant).

After devising test cases and reviewing the similar examples, plan a step by step approach for implementing an algorithm which solves the problem (don't worry about efficiency yet).

Next, proceed to write your algorithm and then check it against the pre-selected test examples. After your algorithm fails it is recommend that you call "py-clear-and-execute-persist" in your next pass to reset your python environment.

If your algorithm passes the tests, then optimize the algorithm and repeat the tests. Because this is a leetcode problem, it is likely that a relatively efficient solution exists. If your algorithm fails the tests, then proceed to modify the algorithm until all test cases are passed. Reflect carefully after each failure, and do not be afried to completely change your approach.

Finally, return the final result as a python markdown snippet using `call_termination`. Lastly, remember that passed newline chars should be double-escaped, like \\n.
"""
