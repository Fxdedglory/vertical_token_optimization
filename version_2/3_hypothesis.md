# 3. Hypothesis

H₀ (Null)
There is no difference in mean total response time between standard and vertical_optimized formatting.
μ_standard = μ_vertical_optimized

H₁ (Alternative)
Vertical_optimized formatting results in lower mean total response time.
μ_vertical_optimized < μ_standard (one-tailed)

Secondary Hypotheses
- H₁a: first_token_ms reduced by ≥30%
- H₁b: estimated_tokens reduced by ≥10%

Statistical Tests
Primary: Welch's two-sample t-test (unequal variances)
Backup: Mann-Whitney U (non-parametric)
Effect size: Cohen's d
Significance level: α = 0.001

Expected Outcome: Reject H₀ with p < 1e-20