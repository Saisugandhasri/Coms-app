def build_prompt(topic: str) -> str:
    return f"""
You are a JSON generator.

Rules:
- Respond ONLY with valid JSON
- No explanations
- No markdown
- Keep paragraph under 80 words

Task:
Generate:
1. One short paragraph on "{topic}"
2. Exactly 5 MCQs

JSON format:
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
