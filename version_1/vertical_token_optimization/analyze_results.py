import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import os
import glob

csv_file = max(glob.glob("results/*.csv"), key=os.path.getctime)
df = pd.read_csv(csv_file)
print(df.groupby("method")[["first_token_ms","total_time","estimated_tokens"]].mean().round(2))

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