import requests
# from app.core.config import LLM_MODEL

OLLAMA_URL = "http://localhost:11434/"

def call_llm(prompt: str) -> str:
    payload = {
        "model": "qwen2.5",
        "prompt": prompt,
        "stream": False,
        "format": "json"
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload,timeout=60)
        response.raise_for_status()
        return response.json()["response"]
    except requests.exceptions.RequestException as e:
        raise RuntimeError(
            f"LLM service unavailable: {str(e)}"
        )
