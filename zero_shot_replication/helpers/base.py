"""Base classes and enums for zero-shot replication problems."""
import textwrap
from enum import Enum


class ProblemType(Enum):
    """Type of problem to generate"""

    HUMAN_EVAL = "human-eval"
    GSM8K = "GSM8K"


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
