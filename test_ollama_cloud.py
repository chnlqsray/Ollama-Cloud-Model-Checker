"""
Ollama Cloud Model Availability Checker
========================================
Tests all known Ollama Cloud models against your account and reports which
ones are accessible on the free tier.

Setup:
    1. Create a .env file in the same folder with: OLLAMA_API_KEY=your_key_here
    2. Run:  python test_ollama_cloud.py

Get your API key at: https://ollama.com/settings/keys
"""

import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()  # Load variables from .env file into os.environ

OLLAMA_API_KEY = os.environ.get("OLLAMA_API_KEY", "")

BASE_URL  = "https://ollama.com/v1/chat/completions"
TIMEOUT   = 40    # seconds per request (cold-start can be slow)
SLEEP_SEC = 1.5   # pause between requests to respect concurrency limits

MODELS = [
    "gemma4:31b-cloud",
    "qwen3.5:cloud",
    "qwen3.5:397b-cloud",
    "glm-5.1:cloud",
    "minimax-m2.7:cloud",
    "nemotron-3-super:cloud",
    "glm-5:cloud",
    "minimax-m2.5:cloud",
    "glm-4.7:cloud",
    "gemini-3-flash-preview:latest",
    "gemini-3-flash-preview:cloud",
    "qwen3-coder-next:cloud",
    "minimax-m2.1:cloud",
    "kimi-k2.6:cloud",
    "deepseek-v3.2:cloud",
    "ministral-3:3b-cloud",
    "ministral-3:8b-cloud",
    "ministral-3:14b-cloud",
    "devstral-small-2:24b-cloud",
    "deepseek-v4-flash:cloud",
    "deepseek-v4-pro:cloud",
    "qwen3-next:80b-cloud",
    "nemotron-3-nano:30b-cloud",
    "rnj-1:8b-cloud",
    "kimi-k2.5:cloud",
    "devstral-2:123b-cloud",
    "mistral-large-3:675b-cloud",
    "gpt-oss:20b-cloud",
    "gpt-oss:120b-cloud",
    "qwen3-vl:235b-cloud",
    "qwen3-vl:235b-instruct-cloud",
    "qwen3-coder:480b-cloud",
    "kimi-k2-thinking:cloud",
    "minimax-m2:cloud",
    "glm-4.6:cloud",
    "deepseek-v3.1:671b-cloud",
    "cogito-2.1:671b-cloud",
    "kimi-k2:1t-cloud",
    "gemma3:4b-cloud",
    "gemma3:12b-cloud",
    "gemma3:27b-cloud",
]


def test_model(model: str) -> tuple[str, str]:
    """
    Send a minimal 1-token request to check model availability.
    Returns (status, detail) where status is "ok", "subscription", or "error".
    """
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": "1"}],
        "max_tokens": 1,
        "stream": False,
    }
    headers = {
        "Authorization": f"Bearer {OLLAMA_API_KEY}",
        "Content-Type": "application/json",
    }
    try:
        r = requests.post(BASE_URL, json=payload, headers=headers, timeout=TIMEOUT)
        if r.status_code == 200:
            return "ok", ""
        elif r.status_code == 403:
            return "subscription", "requires subscription"
        elif r.status_code == 404:
            return "error", "model not found (404)"
        elif r.status_code == 429:
            return "error", "rate limited (429) – try again later"
        else:
            try:
                msg = r.json().get("error", r.text[:100])
            except Exception:
                msg = r.text[:100]
            return "error", f"HTTP {r.status_code}: {msg}"
    except requests.exceptions.Timeout:
        return "error", f"timeout (>{TIMEOUT}s)"
    except Exception as e:
        return "error", str(e)[:100]


def main() -> None:
    print(f"Testing {len(MODELS)} models  |  {SLEEP_SEC}s delay between requests\n")
    print("=" * 65)

    ok_list:  list[str]             = []
    sub_list: list[str]             = []
    err_list: list[tuple[str, str]] = []

    for i, model in enumerate(MODELS, 1):
        print(f"[{i:02d}/{len(MODELS)}] {model} ...", end=" ", flush=True)
        status, detail = test_model(model)

        if status == "ok":
            print("✅  available")
            ok_list.append(model)
        elif status == "subscription":
            print("❌  subscription required")
            sub_list.append(model)
        else:
            print(f"⚠   {detail}")
            err_list.append((model, detail))

        if i < len(MODELS):
            time.sleep(SLEEP_SEC)

    print("\n" + "=" * 65)
    print(f"✅  FREE / AVAILABLE  ({len(ok_list)} models):")
    for m in ok_list:
        print(f"    {m}")

    print(f"\n❌  SUBSCRIPTION REQUIRED  ({len(sub_list)} models):")
    for m in sub_list:
        print(f"    {m}")

    if err_list:
        print(f"\n⚠   OTHER ERRORS  ({len(err_list)} models):")
        for m, d in err_list:
            print(f"    {m}  →  {d}")

    print("\nDone.")


if __name__ == "__main__":
    if not OLLAMA_API_KEY:
        print(
            "ERROR: API key not found.\n"
            "Create a .env file in the same folder with this content:\n"
            "    OLLAMA_API_KEY=your_key_here\n"
            "Get your key at: https://ollama.com/settings/keys"
        )
    else:
        main()
