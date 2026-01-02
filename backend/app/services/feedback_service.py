import requests
import json

from app.prompts.image_prompt import feedback_prompt


def evaluate_speech(image_context: str, audio_text: str):
    prompt = feedback_prompt(image_context,audio_text)

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.2",
            "prompt": prompt,
            "stream": False
        }
    )

    result = response.json()["response"]

    # optional: ensure valid JSON
    try:
        return json.loads(result)
    except:
        return {"error": "Model did not return valid JSON", "raw": result}