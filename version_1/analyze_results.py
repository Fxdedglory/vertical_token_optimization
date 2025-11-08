# 1) Install deps (Conda)
conda install -y pandas matplotlib

# 2) Write analyze_results.py (UTF-8 safe)
@'
import os, sys, math, datetime
import pandas as pd
import matplotlib.pyplot as plt

# ---- Inputs / paths ----
csv_path = sys.argv[1] if len(sys.argv) > 1 else r"benchmark_v2/results/latency_comparison.csv"
if not os.path.exists(csv_path):
    raise FileNotFoundError(f"CSV not found: {csv_path}")

results_dir = os.path.dirname(csv_path)
summary_md = os.path.join(results_dir, "summary.md")
lat_png = os.path.join(results_dir, "latency_avg.png")
tok_png = os.path.join(results_dir, "tokens_avg.png")
use_cases_md = os.path.join(results_dir, "use_cases.md")  # will append rows here

# ---- Load ----
df = pd.read_csv(csv_path)
# Ensure expected columns exist
required = {"timestamp","model","trial","latency_s","tokens"}
missing = required - set(df.columns)
if missing:
    raise ValueError(f"Missing columns in CSV: {missing}")

# ---- Aggregate ----
agg = (
    df.groupby("model", as_index=False)
      .agg(trials=("latency_s","count"),
           avg_latency=("latency_s","mean"),
           avg_tokens=("tokens","mean"))
)
# Round for display
agg["avg_latency"] = agg["avg_latency"].round(3)
agg["avg_tokens"]  = agg["avg_tokens"].round(1)

# ---- Write Markdown summary ----
lines = []
lines.append(f"# Benchmark Summary ({datetime.datetime.now().isoformat(timespec='seconds')})")
lines.append("")
lines.append(f"**Source CSV:** `{os.path.relpath(csv_path).replace(os.sep,'/')}`")
lines.append("")
lines.append("| model | trials | avg_latency_s | avg_tokens |")
lines.append("|-------|--------|---------------|------------|")
for _, r in agg.iterrows():
    lines.append(f"| {r['model']} | {int(r['trials'])} | {r['avg_latency']:.3f} | {r['avg_tokens']:.1f} |")
with open(summary_md, "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")

# ---- Plots ----
# (No explicit colors or styles; defaults only)
plt.figure()
plt.bar(agg["model"], agg["avg_latency"])
plt.ylabel("Avg Latency (s)")
plt.title("Avg Latency by Model")
plt.tight_layout()
plt.savefig(lat_png, dpi=150)
plt.close()

plt.figure()
plt.bar(agg["model"], agg["avg_tokens"])
plt.ylabel("Avg Tokens")
plt.title("Avg Tokens by Model")
plt.tight_layout()
plt.savefig(tok_png, dpi=150)
plt.close()

# ---- Append to use_cases.md (create if missing)
# Existing header (from earlier): | model | trials | avg_latency | token_efficiency | notes |
# We'll compute a simple token_efficiency = avg_tokens / avg_latency (tokens/sec)
need_header = not os.path.exists(use_cases_md) or os.path.getsize(use_cases_md) == 0
rows = []
if need_header:
    rows.append("| model | trials | avg_latency | token_efficiency | notes |")
    rows.append("|-------|--------|-------------|------------------|-------|")

for _, r in agg.iterrows():
    eff = (r["avg_tokens"] / r["avg_latency"]) if r["avg_latency"] > 0 else float("nan")
    rows.append(f"| {r['model']} | {int(r['trials'])} | {r['avg_latency']:.3f} | {eff:.2f} | auto-appended |")

with open(use_cases_md, "a", encoding="utf-8") as f:
    if rows:
        f.write("\n".join(rows) + "\n")

print("Wrote:", os.path.relpath(summary_md))
print("Saved:", os.path.relpath(lat_png), "and", os.path.relpath(tok_png))
print("Updated:", os.path.relpath(use_cases_md))
'@ | Set-Content .\benchmark_v2\src\analyze_results.py -Encoding UTF8

# 3) Run analysis (reads benchmark_v2/results/latency_comparison.csv)
python .\benchmark_v2\src\analyze_results.py

# 4) Stage, commit, push artifacts
git add .\benchmark_v2\results\summary.md .\benchmark_v2\results\latency_avg.png .\benchmark_v2\results\tokens_avg.png .\benchmark_v2\src\analyze_results.py .\benchmark_v2\results\use_cases.md
git commit -m "bench: add analysis summary + plots (avg latency/tokens) and update use_cases table"
git push origin main
