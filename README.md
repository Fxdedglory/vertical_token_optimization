
 # Vertical Token Optimization

Measure how **prompt density** (sparse → medium → dense) affects LLM latency and token usage.

**Repo:** https://github.com/Fxdedglory/vertical_token_optimization  
**Author:** fxdedglory  
**Date:** November 07, 2025

---

## Hypothesis
There is a token cost savings if you remove vertical spacing. More specifically, if you force a new line as the first character then have a "header" two lines you save some tokens and have a quicker response time.

## Introduction
I differentiate between three densities.

- **Sparse (control):** roomy paragraphs, extra blank lines.
- **Medium (typical):** compact but readable.
- **Dense (treatment):** forced first newline then two tight lines, no extra whitespace.

## Method
For each style and model, I run multiple trials (50) and aggregated the response time and tokens generated:
- **Avg. Response Time (s)** – how long a full reply takes
- **Avg. Tokens** – tokens generated (proxy for cost)

*raw data can be found in the /data folder in .csv format
---

## Results

- **Summary (by model × prompt style):** `results/summary.md`
- **Final pivot tables:** `results/final_table.md`
  - `## Avg. Response Time (s)`
  - `## Avg. Tokens`
- **Charts:**  
  - `results/latency_by_style.png`  
  - `results/tokens_by_style.png`

# Results Table

## Avg. Response Time (s)

| model   |   dense |   medium |   smoke |   sparse |
|:--------|--------:|---------:|--------:|---------:|
| chatgpt |   0.805 |    0.8   |   0.801 |    0.807 |
| grok    |   0.954 |    0.952 |   0.946 |    0.954 |

## Avg. Tokens

| model   |   dense |   medium |   smoke |   sparse |
|:--------|--------:|---------:|--------:|---------:|
| chatgpt |     250 |      250 |     250 |      250 |
| grok    |     265 |      265 |     265 |      265 |


---
## Conclusion

There is insufficient evidence to prove that "smushing" tokens together into a forced newline header section decreases the response time or uses less tokens.  

## Observations
Grok uses slightly more tokens than ChatGPT for the same queries




## How to reproduce
1. **Environment**
   ```bash
   conda env update -n vertical -f infrastructure/environment.yml --prune
   conda activate vertical
