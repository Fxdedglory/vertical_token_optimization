import os, time, csv, json, random, statistics
from datetime import datetime
from tqdm import tqdm

# --- Config (env-overridable) ---
TRIALS = int(os.getenv("TRIALS", "50"))
PROMPT = os.getenv("PROMPT", "Summarize the implications of vertical token packing for latency optimization.")
PER_REQUEST_DELAY = float(os.getenv("PER_REQUEST_DELAY", "0.2"))  # small throttle between calls
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "6"))
USE_MOCK_CHATGPT = os.getenv("USE_MOCK_CHATGPT", "0") == "1"     # set to 1 to bypass API during quota/rate limits

MODELS = {
    "chatgpt": {"name": os.getenv("OPENAI_MODEL", "gpt-4o-mini"), "provider": "openai"},
    "grok":    {"name": os.getenv("GROK_MODEL", "grok-2"),       "provider": "xai"}  # still mocked below
}

# --- Lazy import OpenAI only if needed ---
client = None
def _get_openai_client():
    global client
    if client is None:
        from openai import OpenAI
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY not set")
        client = OpenAI(api_key=api_key)
    return client

def _retry(fn, *args, **kwargs):
    delay = 1.0
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            msg = str(e)
            # back off on rate/429/network-ish
            if "RateLimit" in msg or "429" in msg or "timeout" in msg or "connection" in msg.lower():
                if attempt == MAX_RETRIES:
                    raise
                time.sleep(delay)
                delay *= 2
            else:
                # non-retryable
                raise

def call_chatgpt(prompt: str):
    if USE_MOCK_CHATGPT:
        # Mock: emulate realistic latency + token size
        start = time.time()
        time.sleep(random.uniform(0.55, 1.1))
        fake_tokens = random.randint(220, 280)
        return time.time() - start, fake_tokens

    def _do():
        c = _get_openai_client()
        start = time.time()
        resp = c.chat.completions.create(
            model=MODELS["chatgpt"]["name"],
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        latency = time.time() - start
        text = resp.choices[0].message.content or ""
        # simple token proxy by whitespace; replace with tiktoken if desired
        tokens = len(text.split())
        return latency, tokens

    return _retry(_do)

def call_grok(prompt: str):
    # Still mocked (replace with xAI SDK when you’re ready)
    start = time.time()
    time.sleep(random.uniform(0.7, 1.2))
    fake_tokens = random.randint(230, 300)
    return time.time() - start, fake_tokens

# --- Ensure output path ---
os.makedirs("benchmark_v2/results", exist_ok=True)
csv_path = "benchmark_v2/results/latency_comparison.csv"

# --- Write header (idempotent) ---
need_header = not os.path.exists(csv_path) or os.path.getsize(csv_path) == 0
with open(csv_path, "a", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    if need_header:
        writer.writerow(["timestamp","model","trial","latency_s","tokens"])

# --- Run trials ---
for model in ("chatgpt", "grok"):
    for trial in tqdm(range(1, TRIALS + 1), desc=f"Running {model}", ncols=100):
        latency, tokens = (call_chatgpt(PROMPT) if model == "chatgpt" else call_grok(PROMPT))
        with open(csv_path, "a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow([datetime.now().isoformat(), model, trial, round(latency,3), tokens])
        if PER_REQUEST_DELAY > 0:
            time.sleep(PER_REQUEST_DELAY)

# --- Summarize ---
with open(csv_path, encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

summary = {}
for model in MODELS:
    lats = [float(r["latency_s"]) for r in rows if r["model"] == model][-TRIALS:]  # last run slice
    toks = [int(r["tokens"]) for r in rows if r["model"] == model][-TRIALS:]
    if lats and toks:
        summary[model] = {
            "avg_latency": round(statistics.mean(lats), 3),
            "avg_tokens":  round(statistics.mean(toks), 1),
            "n": len(lats)
        }

print("\nResults:")
print(json.dumps(summary, indent=2))
