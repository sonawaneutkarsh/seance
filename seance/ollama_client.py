"""Minimal Ollama client (stdlib only). Returns None when no model is reachable,
so callers can fall back to the deterministic spirits instead of erroring.
"""

import json
import urllib.request

OLLAMA_URL = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "gemma3"


def ask_model(prompt, model=DEFAULT_MODEL, timeout=30):
    """Ask a local open-weight model. Returns its text, or None on any failure."""
    payload = json.dumps(
        {"model": model, "prompt": prompt, "stream": False}
    ).encode()
    request = urllib.request.Request(
        OLLAMA_URL, data=payload, headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read())["response"].strip()
    except Exception:
        return None
