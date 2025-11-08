Vertical Token Optimization
30% Faster LLM Responses via First-Token + Dense-Line Packing

Repository: https://github.com/fxdedglory/vertical-token-optimization
Author: fxdedglory
Date: November 07, 2025
Status: NULL HYPOTHESIS REJECTED (p < 1e-25)

CLAIM
Forcing leading \n + exactly 2 dense lines (~170 tokens each) reduces:
- Time to first token: -32%
- Total latency:       -30%
- Token usage & cost:  -11%
- Statistical significance: p < 1e-25 (n=200+), Effect size (Cohen's d): > 2.8

DATA SCIENCE LIFECYCLE (version_3)
- Business Understanding → version_3/lifecycle/1_business_understanding.md
- Data Acquisition      → version_3/lifecycle/2_data.md
- Hypothesis            → version_3/lifecycle/3_hypothesis.md
- Modeling & Experiment → version_3/lifecycle/4_modeling_experimentation.md
- Evaluation            → version_3/lifecycle/5_evaluation.md
- Deployment & Monitor  → version_3/lifecycle/6_deployment_monitoring.md

RESULTS
- version_3/results/summary.md
- version_3/results/final_table.md  (per-model × prompt-style tables)
- version_3/results/latency_by_style.png
- version_3/results/tokens_by_style.png

Prompt Profiles
- Sparse → version_3/prompts/prompt_sparse.txt
- Medium → version_3/prompts/prompt_medium.txt
- Dense  → version_3/prompts/prompt_dense.txt

HOW TO RUN
conda env update -n vertical -f version_3/infrastructure/environment.yml --prune
conda activate vertical
python version_3/scripts/run_full_benchmark.py 50 --prompt version_3/prompts/prompt_dense.txt  --tag dense
python version_3/scripts/run_full_benchmark.py 50 --prompt version_3/prompts/prompt_medium.txt --tag medium
python version_3/scripts/run_full_benchmark.py 50 --prompt version_3/prompts/prompt_sparse.txt --tag sparse
python version_3/scripts/analyze_results.py

PRODUCTION PROMPT TEMPLATE
\n[170 tokens dense output no newlines][remaining tokens]LOCAL_REFORMAT=true
