import os
import time
import json
import requests
from dotenv import load_dotenv
load_dotenv()

def run_standard(prompt):
    start = time.time()
    first_token_time = None
    content = ""
    response = requests.post(
        "https://api.x.ai/v1/chat/completions",
        headers={"Authorization": f"Bearer {os.getenv('GROK_API_KEY')}"},
        json={
            "model": "grok-4",
            "messages": [{"role": "user", "content": prompt}],
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
            # GROK SENDS "data:{" OR "data: {" — NO SPACE ON FIRST CHUNK
            if raw.startswith("data:"):
                raw = raw[5:]  # Remove "data:" or "data: "
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
        "method": "standard",
        "first_token_ms": round((first_token_time - start) * 1000, 1) if first_token_time else 999,
        "total_time": round(total_time, 3),
        "estimated_tokens": int(tokens)
    }