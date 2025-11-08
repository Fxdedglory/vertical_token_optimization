import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import os
import glob
from pathlib import Path

csv_file = max(glob.glob("results/*.csv"), key=os.path.getctime)
df = pd.read_csv(csv_file)
print(df.groupby("method")[["first_token_ms","total_time","estimated_tokens"]].mean().round(2))

rows = []
for p in Path(".").rglob("*.csv"):
    if "benchmark" in p.name or "latency" in p.name:
        try:
            df = pd.read_csv(p)
            # Expect columns: model, latency_s, tokens, style
            if {"model","latency_s","tokens","style"}.issubset(df.columns):
                rows.append(df[["model","latency_s","tokens","style"]])
        except Exception:
            pass

df = pd.concat(rows, ignore_index=True)
agg = df.groupby(["model","style"], as_index=False).agg(
    trials=("latency_s","count"),
    avg_latency=("latency_s","mean"),
    avg_tokens=("tokens","mean"),
)

# Save a single consolidated table
out = Path("results") ; out.mkdir(exist_ok=True, parents=True)
agg.to_csv(out / "final_table.csv", index=False)

# Also write a md pretty table
md = ["| model | style | trials | avg_latency (s) | avg_tokens |",
      "|-------|-------|-------:|-----------------:|-----------:|"]
for r in agg.itertuples(index=False):
    md.append(f"| {r.model} | {r.style} | {r.trials} | {r.avg_latency:.3f} | {r.avg_tokens:.1f} |")
(out / "final_table.md").write_text("\n".join(md), encoding="utf-8")


v = df[df.method=="vertical_optimized"].total_time.dropna()
s = df[df.method=="standard"].total_time.dropna()
p = stats.ttest_ind(v, s).pvalue
cohens_d = (v.mean() - s.mean()) / ((v.std()**2 + s.std()**2)/2)**0.5

print(f"\nStatistical significance: p = {p:.2e}")
print(f"Cohen's d = {cohens_d:.2f}")

df.boxplot(column="total_time", by="method")
plt.title("Total Response Time: Vertical vs Standard")
plt.suptitle("")
plt.ylabel("Seconds")
plt.savefig("results/latency_proof.png", dpi=300, bbox_inches="tight")
plt.close()
print("Chart saved: results/latency_proof.png")