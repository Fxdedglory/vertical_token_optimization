import sys
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
csv_path = ROOT / "results" / "latency_comparison.csv"
out_dir = ROOT / "results"
out_dir.mkdir(parents=True, exist_ok=True)

if not csv_path.exists():
    print(f"CSV not found: {csv_path}")
    sys.exit(1)

df = pd.read_csv(csv_path)

if df.empty or not set(["model","latency_s","tokens"]).issubset(df.columns):
    print("| model | avg_latency (s) | avg_tokens |\n|--------|-----------------|-------------|\n")
    print("No rows to summarize (CSV empty or missing columns).")
    sys.exit(0)

# === Aggregates ===
trials = df.groupby("model")["latency_s"].count().rename("trials")
summary = df.groupby("model")[["latency_s","tokens"]].mean().round({"latency_s":3,"tokens":1})
summary = pd.concat([trials, summary], axis=1).reset_index()
summary = summary.rename(columns={"latency_s":"avg_latency","tokens":"avg_tokens"})

# === Markdown outputs ===
md = "| model | trials | avg_latency (s) | avg_tokens |\n|-------|--------:|-----------------:|-----------:|\n"
for _, r in summary.iterrows():
    md += f"| {r.model} | {int(r.trials)} | {r.avg_latency:.3f} | {r.avg_tokens:.1f} |\n"

(out_dir / "summary.md").write_text(md, encoding="utf-8")
(out_dir / "final_table.md").write_text(md, encoding="utf-8")
print(md)

# === Chart 1: Latency bars ===
plt.figure(figsize=(7,4))
plt.bar(summary["model"], summary["avg_latency"])
plt.title("Average Latency by Model")
plt.ylabel("Seconds")
plt.tight_layout()
plt.savefig(out_dir / "latency_plot.png", dpi=150)
plt.close()

# === Chart 2: Dual-axis (latency bars + tokens line) ===
fig, ax1 = plt.subplots(figsize=(8,4))
ax2 = ax1.twinx()
ax1.bar(summary["model"], summary["avg_latency"])
ax2.plot(summary["model"], summary["avg_tokens"], marker="o")

ax1.set_title("Latency (bars) vs Tokens (line)")
ax1.set_ylabel("Avg Latency (s)")
ax2.set_ylabel("Avg Tokens")

fig.tight_layout()
plt.savefig(out_dir / "latency_tokens_dual.png", dpi=150)
plt.close()

print(f"\nSaved:\n - {out_dir/'summary.md'}\n - {out_dir/'final_table.md'}\n - {out_dir/'latency_plot.png'}\n - {out_dir/'latency_tokens_dual.png'}")
