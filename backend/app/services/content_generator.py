import json
from app.core.llm_client import call_llm
from app.prompts.mcq_prompt import build_prompt


def generate_content(topic: str) -> dict:
    prompt = build_prompt(topic)
    raw_output = call_llm(prompt)

    try:
        data = json.loads(raw_output)
    except json.JSONDecodeError:
        raise ValueError("LLM did not return valid JSON")

    if "paragraph" not in data or "mcqs" not in data:
        raise ValueError("Invalid LLM response structure")

    if len(data["mcqs"]) != 5:
        raise ValueError("Expected exactly 5 MCQs")

    return data
