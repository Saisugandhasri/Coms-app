import requests
import json
import re

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "llama3.1:8b"


def extract_json(text: str):
    """
    Safely extract JSON from LLM output
    """
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            return json.loads(match.group())
        raise ValueError("LLM did not return valid JSON")


def generate_tense_question():
    prompt = """
You MUST generate a grammatically INCORRECT English sentence.

Rules (DO NOT BREAK THESE):
1. The sentence MUST contain a clear time marker (yesterday, last week, tomorrow, already, etc.)
2. The verb tense MUST NOT match the time marker
3. The sentence MUST be WRONG grammatically
4. DO NOT explain the mistake
5. DO NOT generate a correct sentence

If the sentence is grammatically correct, the output is INVALID.

Respond ONLY in JSON:
{
  "sentence": "incorrect sentence here",
  "topic": "wrong tense used"
}
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3,
            "stream": False
        }
    )

    response.raise_for_status()
    data = response.json()

    content = data["message"]["content"]
    return extract_json(content)




def evaluate_answer(sentence: str, user_answer: str):
    prompt = f"""
    Original sentence:
    "{sentence}"

    User answer:
    "{user_answer}"

    Evaluate the answer.

    Respond ONLY in JSON:
    {{
      "is_correct": true or false,
      "mistakes": ["..."],
      "corrected_sentence": "...",
      "feedback": "Detailed explanation"
    }}
    """

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "stream": False
        }
    )

    response.raise_for_status()
    data = response.json()

    content = data["message"]["content"]
    return extract_json(content)
