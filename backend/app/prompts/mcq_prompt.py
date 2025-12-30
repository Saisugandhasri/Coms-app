def build_prompt(topic: str) -> str:
    return f"""
Generate:
1. A short paragraph on "{topic}"
2. Exactly 5 MCQs

Return ONLY valid JSON in this format:

{{
  "paragraph": "...",
  "mcqs": [
    {{
      "question": "...",
      "options": {{
        "A": "...",
        "B": "...",
        "C": "...",
        "D": "..."
      }},
      "correct_answer": "A"
    }}
  ]
}}
"""
