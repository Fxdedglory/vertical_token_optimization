import os
import time
import json
import requests
from dotenv import load_dotenv
load_dotenv()

def run_vertical(prompt):
    vp = f"\n{prompt}\n\nCRITICAL FORMATTING RULES - OBEY EXACTLY:\nLine 1: single newline character only\nLine 2: first 180 tokens of response (dense, no newlines, no markdown)\nLine 3: remaining tokens (no trailing newline)\nNO explanations, NO code blocks, NO extra text."
    start = time.time()
    first_token_time = None
    content = ""
    response = requests.post(
        "https://api.x.ai/v1/chat/completions",
        headers={"Authorization": f"Bearer {os.getenv('GROK_API_KEY')}"},
        json={
            "model": "grok-4",
            "messages": [{"role": "user", "content": vp}],
            "temperature": 0,
            "max_tokens": 4096,
            "stream": True,
            "stream_options": {"include_usage": True}
        },
        stream=True,
        timeout=120
    )
    for line in response.iter_lines():
        if line:
            raw = line.decode("utf-8")
            if raw.startswith("data:"):
                raw = raw[5:]
            if raw.strip() == "[DONE]":
                break
            try:
                data = json.loads(raw)
                delta = data["choices"][0]["delta"].get("content", "")
                if delta:
                    content += delta
                    if first_token_time is None:
                        first_token_time = time.time()
            except:
                continue
    total_time = time.time() - start
    tokens = len(content.encode("utf-8")) // 4 + 30
    return {
        "method": "vertical_optimized",
        "first_token_ms": round((first_token_time - start) * 1000, 1) if first_token_time else 999,
        "total_time": round(total_time, 3),
        "estimated_tokens": int(tokens)
    }