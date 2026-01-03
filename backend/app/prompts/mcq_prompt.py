def build_prompt(topic: str) -> str:
    return f"""You are an educational content generator and strict JSON generator.

GLOBAL RULES (MANDATORY):
- Respond ONLY with valid JSON
- Do NOT include explanations, markdown, comments, or extra text
- Do NOT include line breaks outside JSON strings
- Ensure the JSON is syntactically valid
- Paragraph length must be at-least 150 words and can range upto 300 words
- Language must be clear, neutral, and learner-friendly

CONTENT OBJECTIVE:
Your goal is to improve the user's reading comprehension skills.
The content must encourage:
- Understanding of main ideas
- Identification of key details
- Logical inference
- Vocabulary-in-context understanding
- Cause-and-effect reasoning

TASK:
1. Generate ONE informative paragraph on the topic: "{topic}"
   - The paragraph must:
     - Introduce the topic clearly
     - Contain at least one implicit idea (not directly stated but inferable)
     - Use 1–2 moderately challenging words that can be understood from context
     - Maintain logical flow and coherence

2. Generate EXACTLY 5 multiple-choice questions (MCQs) based ONLY on the paragraph
   - Each MCQ must test a different comprehension skill:
     1. Main idea / central theme
     2. Specific factual detail
     3. Vocabulary-in-context meaning
     4. Logical inference (unstated conclusion)
     5. Cause-and-effect or reasoning
   - Each question must have 4 options (A, B, C, D)
   - Only ONE option must be correct
   - Incorrect options must be plausible but clearly wrong on close reading
   - The correct answer must be evenly distributed (do not always use "A")
3. Generate EXACTLY 3 one-word questions based ONLY on the paragraph

OUTPUT FORMAT (STRICT):
{{
  "paragraph": "<paragraph text>",
  "mcqs": [
    {{
      "question": "<question text>",
      "options": {{
        "A": "<option text>",
        "B": "<option text>",
        "C": "<option text>",
        "D": "<option text>"
      }},
      "correct_answer": "<A | B | C | D>"
    }}
  ],
    "one_word_questions": [
    {{
      "question": "<question text>",
      "answer": "<single_word_answer>"
    }}
  ]
}}

FINAL CHECK BEFORE RESPONDING:
- Output ONLY the JSON object
- Ensure EXACTLY 5 MCQs
- Ensure EXACTLY 3 one-word questions
- Ensure paragraph is at-least 150 words
- Ensure all questions are answerable strictly from the paragraph
"""
