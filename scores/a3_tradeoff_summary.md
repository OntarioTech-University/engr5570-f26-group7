PyExamine 0.3.0, 34 programs, outputs folder `outputs`, condition `single`

| Version | Mean max CC | Mean total CC | Mean functions | Long Method | Long Parameter List | Data Clumps | All smells |
|---|---:|---:|---:|---:|---:|---:|---:|
| original | 11.29 | 14.65 | 1.53 | 8 | 2 | 0 | 11 |
| gpt | 6.62 | 15.97 | 3.21 | 0 | 8 | 2 | 11 |
| deepseek | 5.41 | 18.41 | 5.24 | 0 | 14 | 4 | 19 |
| qwen | 5.53 | 17.94 | 5.09 | 0 | 15 | 4 | 20 |

Runs where the highest complexity went down and the smells went up, and runs where the total complexity went up:

| Model | Runs | Max CC down and smells up | Total CC up |
|---|---:|---:|---:|
| gpt | 34 | 4 | 22 |
| deepseek | 34 | 5 | 31 |
| qwen | 34 | 5 | 28 |
