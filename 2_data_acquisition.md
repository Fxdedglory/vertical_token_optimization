# 2. Data Acquisition

Data Source: xAI Grok API[](https://api.x.ai/v1/chat/completions)
Collection Method: Streaming HTTP POST with real-time chunk parsing
Sample Size: Minimum 100 paired trials per method (200 total)
Power Analysis: 99.9% power to detect 20% difference at α=0.001

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