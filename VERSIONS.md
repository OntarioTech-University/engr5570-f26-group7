# Versions

These are the versions we used for the results in this repository.
The refactoring runs used openai 3.31.0. Python, python-dotenv, radon and
pyarrow below are from a fresh install on a new computer in November 2026,
so they may be slightly different from the versions used for the first runs.

| Tool | Version | Used for |
| --- | --- | --- |
| Python | 3.12.10 | Refactoring runs and tests |
| Python | 3.12 | PyExamine environments, see `scores/README.md` |
| Python | 3.10, 3.11, 3.12, 3.13 | Checking the originals pass all tests, see `data/verification_py*.json` |
| openai | 3.31.0 | Calling the models through OpenRouter |
| python-dotenv | 1.2.4 | Reading the API key from `.env` |
| radon | 6.0.1 | Complexity and size |
| pyarrow | 26.0.1 | Reading the CodeContests parquet files |
| PyExamine 0.2.3 | commit `fd6d9f971c8eb577a5686da0e0c283e81edc0695` | A2 code smell scores |
| PyExamine 0.3.0 | commit `838b212fafe9b1ff1e06c3364892e53177dab16f` | A3 code smell analysis |

## Models

All models were called through OpenRouter with temperature 0 and max_tokens 32,000.

| Short name | Model ID |
| --- | --- |
| qwen | qwen/qwen3.8-max-0902 |
| deepseek | deepseek/deepseek-v4-pro-0813 |
| gpt | openai/gpt-6-sol |

The model ID for each run is saved in its `summary.json`.

## Data

| Source | Version |
| --- | --- |
| ASE replication package | Zenodo DOI 10.5281/zenodo.19245562, `replication_package.zip`, MD5 `c33a26b249f9bafcc7bdd2cc2cf2f77f` |
| CodeContests | Hugging Face `deepmind/code_contests`, revision `802411c3010cb00d1b05bad57ca77365a3c699d6` |