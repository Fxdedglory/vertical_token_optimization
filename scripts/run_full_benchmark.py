# scripts/run_full_benchmark.py
import argparse, os, time, csv, random, sys
from pathlib import Path

# --- Minimal runner that prefers an explicit --prompt file ---
def load_prompt(args):
    if args.prompt:
        p = Path(args.prompt)
        if not p.exists():
            raise FileNotFoundError(f"Prompt file not found: {p}")
        return p.read_text(encoding="utf-8")
    # Fallbacks only if --prompt wasn't provided:
    try:
        # If you still keep these around, fine; otherwise this branch won't be used.
        from benchmark.prompt_templates import PROMPTS
        # Handle dict vs list
        if isinstance(PROMPTS, dict):
            return random.choice(list(PROMPTS.values()))
        elif isinstance(PROMPTS, (list, tuple)):
            return random.choice(PROMPTS)
        else:
            raise TypeError("PROMPTS must be a dict or list/tuple")
    except Exception:
        # Last-ditch generic prompt
        return "Explain <YOUR TOPIC HERE> clearly with examples."

def simulate_call(model_name: str, prompt_text: str):
    """
    Placeholder for your real model call.
    Replace with actual API calls if desired.
    Returns (latency_seconds, tokens_used).
    """
    # Very basic, randomized timing to produce plausible numbers.
    # Keep deterministic-ish across models for now; the analysis script will still aggregate.
    base = 0.8 if model_name == "chatgpt" else 0.95
    jitter = random.uniform(-0.05, 0.06)
    latency = max(0.15, base + jitter)
    tokens = 250 if model_name == "chatgpt" else 265
    time.sleep(0.01)  # tiny delay to simulate work
    return latency, tokens

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("trials", type=int, help="Number of trials to run")
    ap.add_argument("--prompt", type=str, default=None, help="Path to prompt file")
    ap.add_argument("--tag", type=str, default="untagged", help="Run label (dense|medium|sparse)")
    ap.add_argument("--models", nargs="+", default=["chatgpt","grok"], help="Models to run")
    args = ap.parse_args()

    prompt_text = load_prompt(args)

    out_dir = Path("results")
    out_dir.mkdir(parents=True, exist_ok=True)
    ts = time.strftime("%Y%m%d_%H%M%S")
    out_csv = out_dir / f"benchmark_{args.tag}_{ts}.csv"

    # CSV header
    with out_csv.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["tag","model","trial","latency_s","tokens"])

        for model in args.models:
            for t in range(1, args.trials + 1):
                latency, tokens = simulate_call(model, prompt_text)
                w.writerow([args.tag, model, t, latency, tokens])

    print(f"Wrote {out_csv}")

if __name__ == "__main__":
    main()
