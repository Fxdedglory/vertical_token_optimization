# 4. Modeling & Experimentation

Experiment Design: Paired trials (same prompt, randomized order)
Timing Method: time.time() around streaming response
Token Estimation: len(content.encode()) // 4 (conservative)

Implementation
- benchmark/standard.py → normal PEP-8 output
- benchmark/vertical.py → \n + 2 dense lines (170 tokens each)
- run_full_benchmark.py → orchestrator with tqdm + CSV export

Validation Checks
- Shapiro-Wilk test for normality
- Levene's test for homogeneity of variance
- 95% bootstrap confidence intervals