import requests

from app.prompts.image_prompt import relevance_prompt

IMAGE_CONTEXT = "This description must match the image content the user presented."

def check_relevance(transcript: str):
    prompt = relevance_prompt(transcript)

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llava:latest",
            "prompt": prompt,
            "stream": False
        }
    )

    data = response.json()
    print("DEBUG RELEVANCE RESPONSE:", data)

    text = data.get("response") or data.get("message") or data.get("content") or ""
    if not text:
        return "Unable to evaluate relevance right now."
