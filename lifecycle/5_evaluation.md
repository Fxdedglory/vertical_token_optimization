# 5. Evaluation

**Trials:** 50 per model  
**Prompt family:** vertical vs standard packing (same content)

| model  | trials | avg_latency (s) | avg_tokens |
|--------|-------:|----------------:|-----------:|
| chatgpt | 50    | 0.848           | 254.0      |
| grok    | 50    | 0.938           | 266.3      |

**Findings**
- Latency: ChatGPT is **~9.6% faster** than Grok \[(0.938−0.848)/0.938\].
- Tokens: ChatGPT uses **~4.6% fewer** tokens \[(266.3−254.0)/266.3\].
- Conclusion: For this benchmark run, vertical packing + ChatGPT yields the best speed-token profile.

Artifacts: see **/results** for plots and summary tables.
