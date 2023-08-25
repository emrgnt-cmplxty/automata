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
poetry run python evals/run_gsm8k_eval.py --model=...
```

## MATH

### Generation

```bash
poetry run python runner.py --provider openai --pset math --model gpt-4-0314 --temperature 0.7

poetry run python runner.py --provider openai --pset math --model gpt-4-0613 --temperature 0.7
```

```bash
poetry run python zero_shot_replication/evals/run_math_eval.py  --model=...
```
