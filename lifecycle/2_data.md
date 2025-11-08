# 2_data.md

## Goal
Document sources, schemas, and data quality gates used in vertical-token optimization experiments.

## Sources
- Benchmark CSVs from \ersion_2/benchmark[_v2]/results/*\
- Generated summaries: \summary.md\, \inal_table.md\

## DQ (dbt-expectations-ready)
- Non-null: model, latency_s, tokens
- Ranges: latency_s > 0, tokens > 0
- Freshness: results updated per run

## Notes
This replaces the blank \2_data_acquisition.md\ and \2_data_understanding.md\.

---
## Acquisition notes (merged from 2_data_acquisition.md)

# 2. Data Acquisition

Data Source: xAI Grok API[](https://api.x.ai/v1/chat/completions)
Collection Method: Streaming HTTP POST with real-time chunk parsing
Sample Size: Minimum 100 paired trials per method (200 total)
Power Analysis: 99.9% power to detect 20% difference at Î±=0.001

Variables
Independent: Output formatting (standard vs vertical_optimized)
Dependent:
  - first_token_ms
  - total_time (seconds)
  - estimated_tokens (bytes//4)
Controls: Same prompt, model, temperature, max_tokens per pair

Prompt Suite (10 categories)
- Code generation (short, medium, long)
- Reasoning (8-queens)
- Creative writing
- Data processing
- API integration
- Terminal tools

Output: results/benchmark_YYYY-MM-DD_HHMMSS.csv

---
## Understanding notes (merged from 2_data_understanding.md)

# 2_data_understanding.md


