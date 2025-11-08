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
