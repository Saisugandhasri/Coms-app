import json
from app.core.llm_client import call_llm
from app.prompts.mcq_prompt import build_prompt

def generate_content(topic: str):
    prompt = build_prompt(topic)
    raw_output = call_llm(prompt)

    # Clean up markdown code blocks if present
    clean_output = raw_output.replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(clean_output)
    except json.JSONDecodeError:
        raise ValueError("LLM returned invalid JSON")
