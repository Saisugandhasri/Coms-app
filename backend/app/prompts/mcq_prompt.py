def build_prompt(topic: str) -> str:
    return f"""
Generate a clear educational paragraph on the topic: "{topic}"

Then generate exactly 5 multiple-choice questions based on the paragraph.

Rules:
- Each question must have 4 options
- Clearly mention the correct answer
- Output strictly in JSON format:
{{
  "paragraph": "...",
  "mcqs": [
    {{
      "question": "...",
      "options": ["A", "B", "C", "D"],
      "correct_answer": "..."
    }}
  ]
}}
"""
