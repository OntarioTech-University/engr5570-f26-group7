## Code quality before and after refactoring

| Version | Programs | Mean max CC | Mean nesting | Mean SLOC | Total smells | Passes all hidden tests |
|---|---:|---:|---:|---:|---:|---:|
| original | 34 | 11.29 | 3.85 | 39.0 | 14 | 34/34 |
| gpt | 34 | 6.62 | 2.74 | 41.2 | 17 | 34/34 |
| deepseek | 34 | 5.41 | 2.76 | 45.5 | 25 | 34/34 |
| qwen | 34 | 5.53 | 2.68 | 47.4 | 26 | 34/34 |

## Programs improved / unchanged / worse, against their own original

| Model | max_cc | max_nesting | n_smells | sloc |
|---|---|---|---|---|
| gpt | 29 / 4 / 1 | 21 / 13 / 0 | 8 / 17 / 9 | 7 / 3 / 24 |
| deepseek | 30 / 3 / 1 | 20 / 14 / 0 | 7 / 16 / 11 | 1 / 1 / 32 |
| qwen | 29 / 4 / 1 | 21 / 13 / 0 | 5 / 19 / 10 | 0 / 4 / 30 |

## Running time, same machine and same runner for every version

| Model | Programs timed | Median vs original | Slowest case |
|---|---:|---:|---:|
| gpt | 34 | 1.003x | 1.04x |
| deepseek | 34 | 1.004x | 1.20x |
| qwen | 34 | 1.005x | 1.18x |
