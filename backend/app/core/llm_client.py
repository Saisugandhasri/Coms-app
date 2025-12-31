# import requests
# # from app.core.config import LLM_MODEL

# OLLAMA_URL = "http://localhost:11434/api/generate"

# def call_llm(prompt: str) -> str:
#     payload = {
#         "model": "nuextract",
#         "prompt": prompt,
#         "stream": False,
#         "format": "json"
#     }
#     try:
#         response = requests.post(OLLAMA_URL, json=payload,timeout=60)
#         response.raise_for_status()
#         return response.json()["response"]
#     except requests.exceptions.RequestException as e:
#         raise RuntimeError(
#             f"LLM service unavailable: {str(e)}"
#         )

import requests


def call_llm(prompt: str) -> str:
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2",
                "prompt": prompt,
                "stream": False,
            },
            timeout=180,
        )
        response.raise_for_status()
        return response.json()["response"]
    except Exception as e:
        raise RuntimeError(f"LLM service unavailable: {str(e)}")
