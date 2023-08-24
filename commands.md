# Commands

## HumanEval

### Generation

```bash
poetry run python zero_shot_replication/runner.py --model=gpt-4-0314 --dataset=human-eval

poetry run python zero_shot_replication/runner.py --model=gpt-4-0613 --dataset=human-eval
```

### Evaluation

```bash
poetry run evalplus.evaluate --dataset humaneval --samples=zero-shot-replication/results/openai/human_eval/gpt_4_0314/openai_human_eval__model_eq_gpt_4_0314__temperature_eq_0p7.jsonl  --parallel 4 --min-time-limit 0.5 --gt-time-limit-factor 5

poetry run evalplus.evaluate --dataset humaneval --samples=zero-shot-replication/results/openai/human_eval/gpt_4_0613/openai_human_eval__model_eq_gpt_4_0613__temperature_eq_0p7.jsonl  --parallel 4 --min-time-limit 0.5 --gt-time-limit-factor 5

```
