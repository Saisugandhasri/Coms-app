import requests
# from app.core.config import LLM_MODEL

OLLAMA_URL = "http://localhost:11434/api/generate"

def call_llm(prompt: str) -> str:
    payload = {
        "model": "llama3.2",
        "prompt": prompt,
        "stream": False,
        "format": "json"
    }

    response = requests.post(OLLAMA_URL, json=payload)
    response.raise_for_status()
    return response.json()["response"]
