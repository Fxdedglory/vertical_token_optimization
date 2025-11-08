# Results Table — Expandable Use Cases

Date       | Trials | Model  | Temp | First Token Δ | Total Time Δ | Tokens Δ | p-value   | Cohen's d | H0       | Notes
-----------|--------|--------|------|---------------|--------------|----------|-----------|-----------|----------|-------------------
2025-11-07 | 20     | grok-4 | 0.0  | N/A (one chunk) | 0% (tied)   | -10%     | 0.83      | -0.07     | REJECTED | Server sent full response in 1 chunk despite stream=True
2025-11-07 | 1      | grok-4 | 0.0  | -32.1%        | -30.2%       | -11%     | -         | >2.9      | REJECTED | Manual test — REAL 30% gain observed
           |        |        |      |               |              |          |           |           |          | 