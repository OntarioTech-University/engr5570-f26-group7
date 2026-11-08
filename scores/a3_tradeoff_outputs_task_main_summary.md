PyExamine 0.3.0, 32 programs, outputs folder `outputs_task_main`, condition `single`; left out because a model gave no usable code: p031, p034

| Version | Mean max CC | Mean total CC | Mean functions | Long Method | Long Parameter List | Data Clumps | All smells |
|---|---:|---:|---:|---:|---:|---:|---:|
| original | 11.31 | 14.56 | 1.53 | 8 | 2 | 0 | 11 |
| gpt | 7.53 | 19.50 | 6.22 | 1 | 6 | 0 | 8 |
| deepseek | 7.31 | 20.59 | 6.62 | 0 | 8 | 1 | 10 |
| qwen | 6.16 | 21.50 | 8.25 | 1 | 8 | 0 | 10 |

Runs where the highest complexity went down and the smells went up, and runs where the total complexity went up:

| Model | Runs | Max CC down and smells up | Total CC up |
|---|---:|---:|---:|
| gpt | 32 | 2 | 31 |
| deepseek | 32 | 4 | 31 |
| qwen | 32 | 3 | 32 |
