"""Base classes and enums for zero-shot replication problems."""
import textwrap
from enum import Enum


class ProblemType(Enum):
    """Type of problem to generate"""

    HUMAN_EVAL = "human-eval"
    MATH = "math"


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

MATH_TEMPLATE = textwrap.dedent(
    """
```markdown
### Instruction:
Solve the following mathematical problem:
{TASK_PROMPT}

### Guidelines:
- **Think Step by Step**: Break down the problem and provide a step-by-step reasoning for your solution.
- **Verify Your Solution**: After arriving at a solution, ensure to verify its correctness within your reasoning process.
- **Return the Final Solution**: Conclude with the final answer using `call-termination`. Ensure your solution is presented in BOXED LATEX format, e.g. `$\\boxed{{YOUR_SOLUTION}}$`.
"""
)
