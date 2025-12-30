def build_prompt(topic: str) -> str:
    return f"""
    You are a JSON API.

    Generate:
    1. One short educational paragraph on "{topic}"
    2. Exactly 5 MCQs

    Rules (VERY IMPORTANT):
    - Output ONLY valid JSON
    - No markdown
    - No explanations
    - Each MCQ MUST be an object
    - Each MCQ MUST have:
      - question (string)
      - options (array of 4 strings)
      - correct_answer (string, must match one option)

    JSON format:
    {{
      "paragraph": "...",
      "mcqs": [
        {{
          "question": "...",
          "options": ["A", "B", "C", "D"],
          "correct_answer": "A"
        }}
      ]
    }}
    """
