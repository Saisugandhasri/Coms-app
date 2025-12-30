import json
from app.core.llm_client import call_llm
from app.prompts.mcq_prompt import build_prompt

def generate_content(topic: str):
    prompt = build_prompt(topic)
    raw_output = call_llm(prompt)

    # Clean up markdown code blocks if present
    clean_output = raw_output.replace("```json", "").replace("```", "").strip()

    data = json.loads(clean_output)

    if "paragraph" not in data or "mcqs" not in data:
        raise ValueError("Invalid LLM response")

    valid_mcqs = []
    for mcq in data["mcqs"]:
        if(
            isinstance(mcq, dict)
            and "questions" in mcq
            and "options" in mcq
            and "correct_answer" in mcq
        ):
            valid_mcqs.append(mcq)
    if len(valid_mcqs) < 1:
        raise ValueError("No valid MCQs")
    data["mcqs"] = valid_mcqs
    return data
