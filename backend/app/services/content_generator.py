import json
from app.core.llm_client_R_L import call_llm
from app.prompts.mcq_prompt import build_prompt


def generate_content(topic: str) -> dict:
    prompt = build_prompt(topic)
    raw_output = call_llm(prompt)

    try:
        data = json.loads(raw_output)
    except json.JSONDecodeError:
        raise ValueError("LLM did not return valid JSON")

    # Core checks
    if "paragraph" not in data or "mcqs" not in data or "one_word_questions" not in data:
        raise ValueError("Invalid response structure")

    if len(data["mcqs"]) != 5:
        raise ValueError("Expected exactly 5 MCQs")

    if len(data["one_word_questions"]) != 3:
        raise ValueError("Expected exactly 3 one-word questions")

    # Enforce true one-word answers
    for q in data["one_word_questions"]:
        if " " in q["answer"].strip():
            raise ValueError("One-word answer contains spaces")
    return data
