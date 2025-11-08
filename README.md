# Vertical Token Optimization

Measure how **prompt density** (sparse → medium → dense) affects LLM latency and token usage.

**Repo:** https://github.com/Fxdedglory/vertical_token_optimization  
**Author:** fxdedglory  
**Date:** November 07, 2025

---

## What this actually measures (plain English)

We run the **same content** with three formatting styles:

- **Sparse (control):** roomy paragraphs, extra blank lines.
- **Medium (typical):** compact but readable.
- **Dense (treatment):** forced first newline then two tight lines, no extra whitespace.

For each style and model, we run multiple trials and record:
- **Avg. Response Time (s)** – how long a full reply takes
- **Avg. First Token (ms)** – time to first token (if available)
- **Avg. Tokens** – tokens generated (proxy for cost)

This repo **records outcomes; it doesn’t assume improvements**. Check the tables and plots below for the literal results from your machine and run.

---

## Latest results

See the generated artifacts:

- **Summary (by model × prompt style):** `results/summary.md`
- **Final pivot tables:** `results/final_table.md`
  - `## Avg. Response Time (s)`
  - `## Avg. Tokens`
- **Charts:**  
  - `results/latency_by_style.png`  
  - `results/tokens_by_style.png`

# Final Table

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

> With the multi-profile benchmark now in place, prefer the new **summary** and **final** tables above—they show **sparse / medium / dense** side-by-side for each model.

---

## How to reproduce

1. **Environment**
   ```bash
   conda env update -n vertical -f infrastructure/environment.yml --prune
   conda activate vertical
