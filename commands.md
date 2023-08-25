# Commands

## HumanEval

### HEval Generation

```bash
poetry run python zero_shot_replication/runner.py --model=... --pset=human-eval
```

### HEval Evaluation

```bash
poetry run evalplus.evaluate --dataset humaneval --samples=... --parallel 4 --min-time-limit 0.5 --gt-time-limit-factor 5
```

## LeetCode

### LC Generation

```bash

poetry run python zero_shot_replication/runner.py --model=... --pset=leetcode
```

### LC Evaluation

```bash
poetry run python zero_shot_replication/evals/run_leetcode_eval.py --model=...
```

## GMS8K

### GMS8K Generation

```bash
poetry run python zero_shot_replication/runner.py --model=... --pset=gsm8k
```

### GMS8K Eval

```bash
# run_MATH_eval can service both MATH and GMS8K
poetry run python evals/run_MATH_eval.py --solutions_file_path=...
```

## MATH

### Generation

```bash
poetry run python zero_shot_replication/runner.py --model=... --pset=math
```

```bash
poetry run python zero_shot_replication/evals/run_math_eval.py --solutions_file_path=...
```
