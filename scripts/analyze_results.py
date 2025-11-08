import os, re, glob
import pandas as pd
import matplotlib.pyplot as plt

os.makedirs("results", exist_ok=True)

def load_one(path: str) -> pd.DataFrame:
    # profile from filename: results/benchmark_<profile>_YYYYMMDD_HHMMSS.csv
    m = re.search(r"benchmark_([^_]+)_\d{8}_\d{6}\.csv$", path.replace("\\","/"))
    profile = m.group(1) if m else "unknown"

    df = pd.read_csv(path)

    # Normalize column names (lower, underscores)
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    # Common aliases
    rename_map = {
        "latency_s": "total_time",
        "latency_sec": "total_time",
        "avg_latency_s": "total_time",
        "avg_latency_(s)": "total_time",
        "tokens": "estimated_tokens",
        "avg_tokens": "estimated_tokens",
        "first_token": "first_token_ms",
        "first_token_ms": "first_token_ms",
        "model_name": "model",
    }
    for src, dst in list(rename_map.items()):
        if src in df.columns and dst not in df.columns:
            df = df.rename(columns={src: dst})

    # Ensure required columns exist
    if "model" not in df.columns:
        # best effort: some logs use 'provider' or 'engine'
        for alt in ["provider", "engine", "backend"]:
            if alt in df.columns:
                df = df.rename(columns={alt: "model"})
                break
    for must in ["model", "total_time", "estimated_tokens"]:
        if must not in df.columns:
            raise ValueError(f"{os.path.basename(path)} is missing required column: {must}")

    # Optional: first_token_ms
    if "first_token_ms" not in df.columns:
        df["first_token_ms"] = pd.NA

    df["profile"] = profile
    return df[["model","profile","first_token_ms","total_time","estimated_tokens"]]

# Load all CSVs
paths = sorted(glob.glob("results/benchmark_*.csv"))
if not paths:
    raise SystemExit("No result CSVs found in results/")

dfs = [load_one(p) for p in paths]
data = pd.concat(dfs, ignore_index=True)

# Summary by model + profile
summary = (
    data.groupby(["model","profile"])[["first_token_ms","total_time","estimated_tokens"]]
        .mean()
        .round(3)
        .reset_index()
        .sort_values(["model","profile"])
)

# Human-friendly table like you asked
pretty = summary.rename(columns={
    "model": "Model",
    "profile": "Prompt Style",
    "total_time": "Avg. Response Time (s)",
    "estimated_tokens": "Avg. Tokens",
    "first_token_ms": "Avg. First Token (ms)"
})

# Save CSV + Markdown
summary_csv = "results/summary_table.csv"
pretty.to_csv(summary_csv, index=False)

md_lines = ["# Summary (by model × prompt style)\n"]
md_lines.append(pretty.to_markdown(index=False))
with open("results/summary.md", "w", encoding="utf-8") as f:
    f.write("\n".join(md_lines))

# Also produce a compact comparison table pivoted by prompt style
pivot_latency = summary.pivot(index="model", columns="profile", values="total_time").round(3)
pivot_tokens  = summary.pivot(index="model", columns="profile", values="estimated_tokens").round(1)

with open("results/final_table.md", "w", encoding="utf-8") as f:
    f.write("# Final Table\n\n")
    f.write("## Avg. Response Time (s)\n\n")
    f.write(pivot_latency.to_markdown() + "\n\n")
    f.write("## Avg. Tokens\n\n")
    f.write(pivot_tokens.to_markdown() + "\n")

# Simple plots (one metric per figure)
plt.figure()
for (model), g in summary.groupby("model"):
    # keep a consistent x-order
    order = ["sparse","medium","dense"]
    g = g.set_index("profile").reindex(order).reset_index()
    plt.plot(g["profile"], g["total_time"], marker="o", label=model)
plt.xlabel("Prompt Style"); plt.ylabel("Avg. Response Time (s)")
plt.title("Latency by Prompt Style and Model"); plt.legend()
plt.tight_layout(); plt.savefig("results/latency_by_style.png"); plt.close()

plt.figure()
for (model), g in summary.groupby("model"):
    order = ["sparse","medium","dense"]
    g = g.set_index("profile").reindex(order).reset_index()
    plt.plot(g["profile"], g["estimated_tokens"], marker="o", label=model)
plt.xlabel("Prompt Style"); plt.ylabel("Avg. Tokens")
plt.title("Tokens by Prompt Style and Model"); plt.legend()
plt.tight_layout(); plt.savefig("results/tokens_by_style.png"); plt.close()

print("Wrote:", summary_csv, "results/summary.md", "results/final_table.md",
      "results/latency_by_style.png", "results/tokens_by_style.png")
