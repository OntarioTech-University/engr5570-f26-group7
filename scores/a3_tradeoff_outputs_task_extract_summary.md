PyExamine 0.3.0, 34 programs, outputs folder `outputs_task_extract`, condition `single`

| Version | Mean max CC | Mean total CC | Mean functions | Long Method | Long Parameter List | Data Clumps | All smells |
|---|---:|---:|---:|---:|---:|---:|---:|
| original | 11.29 | 14.65 | 1.53 | 8 | 2 | 0 | 11 |
| gpt | 5.00 | 21.71 | 8.26 | 0 | 20 | 7 | 28 |
| deepseek | 5.24 | 22.82 | 9.00 | 0 | 18 | 5 | 26 |
| qwen | 4.65 | 24.88 | 11.62 | 0 | 27 | 7 | 35 |

Runs where the highest complexity went down and the smells went up, and runs where the total complexity went up:

| Model | Runs | Max CC down and smells up | Total CC up |
|---|---:|---:|---:|
| gpt | 34 | 7 | 34 |
| deepseek | 34 | 8 | 34 |
| qwen | 34 | 9 | 34 |
