# Commands

## HumanEval Generation

gpt-3.5-turbo

```bash
poetry run python zero_shot_replication/runner.py --model=gpt-3.5-turbo-0314 --dataset=human-eval

poetry run python zero_shot_replication/runner.py --model=gpt-3.5-turbo-0613 --dataset=human-eval
```

gpt-4

```bash
poetry run python zero_shot_replication/runner.py --model=gpt-4-0314 --dataset=human-eval

poetry run python zero_shot_replication/runner.py --model=gpt-4-0613 --dataset=human-eval
```

### HumanEval Evaluation

gpt-4

```bash
poetry run evalplus.evaluate --dataset humaneval --samples=zero-shot-replication/results/openai/human_eval/gpt_4_0314/openai_human_eval__model_eq_gpt_4_0314__temperature_eq_0p7_experiment.jsonl  --parallel 4 --min-time-limit 0.5 --gt-time-limit-factor 5
```
