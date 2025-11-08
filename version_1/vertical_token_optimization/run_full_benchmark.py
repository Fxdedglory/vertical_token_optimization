import random
import time
import pandas as pd
from tqdm import tqdm
from benchmark.prompt_templates import PROMPTS
from benchmark.standard import run_standard
from benchmark.vertical import run_vertical

def run(trials=10):
    results = []
    for i in tqdm(range(trials), desc="Running trials"):
        prompt = random.choice(PROMPTS)
        for func, name in [(run_standard, "standard"), (run_vertical, "vertical_optimized")]:
            try:
                r = func(prompt)
                r["trial"] = i
                r["prompt"] = prompt[:100]
                results.append(r)
            except Exception as e:
                print(f"Error in {name}: {e}")
        time.sleep(0.7)
    df = pd.DataFrame(results)
    filename = f"results/benchmark_{time.strftime('%Y-%m-%d_%H%M%S')}.csv"
    df.to_csv(filename, index=False)
    print("\nResults:")
    print(df.groupby("method")[["first_token_ms","total_time","estimated_tokens"]].mean().round(2))
    return df

if __name__ == "__main__":
    import sys
    trials = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    run(trials)