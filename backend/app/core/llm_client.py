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
