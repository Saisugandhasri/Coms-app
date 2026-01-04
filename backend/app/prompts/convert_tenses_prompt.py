def get_convert_tenses_generation_prompt(nonce):
    return f"""
You are an expert English grammar teacher.
You are expert in generating different questions everytime when You are called.

TASK:
Generate EXACTLY 5 English tense-conversion questions for a Tenses practice application.

SESSION ID: {nonce}
This generation must be unique and unrelated to any previous content.
This request is independent from all previous requests.
Do NOT reuse ideas, situations, or sentence patterns from earlier generations.

SCENARIO DIVERSITY (CRITICAL — DO NOT IGNORE):
- Each sentence MUST come from a CLEARLY DIFFERENT real-world situation.
- Think broadly about real life: work, family, health, emotions, technology, weather,
  travel, education, shopping, social events, emergencies, hobbies, news, or personal goals etc....
- Do NOT reuse similar actions, subjects, or storylines.
- Do NOT generate multiple sentences that could happen on the same day or event.
- Each sentence should feel like it belongs to a completely different story.
- Be creative, realistic, and natural.

ANTI-REPETITION RULES (MANDATORY):
- Do NOT use the same subject pattern twice (e.g., avoid repeating "I", "She", "They").
- Do NOT reuse common ESL examples (gym, school, homework, office, vacation).
- Avoid textbook-style or predictable sentences.
- Prefer natural but less obvious, real-life situations.

STRICT RULES:
1. Each sentence MUST be 100% grammatically correct.
2. Each sentence MUST sound natural and commonly used by native speakers.
3. Each sentence MUST be written in ONE clear tense.
4. The target tense MUST be DIFFERENT from the sentence's original tense.
5. Each question MUST have a UNIQUE target tense.
6. You MAY use ANY valid English tense (no restrictions).
7. Do NOT include explanations, hints, or extra text.
8. Do NOT include incorrect or awkward sentences.
9. Respond ONLY in valid JSON.

IMPORTANT:
- Clearly identify the target tense.
- Ensure the sentence tense does NOT already match the target tense.
- Focus on realistic, everyday English usage.

RESPONSE FORMAT (EXACT — DO NOT CHANGE):

{{
  "questions": [
    {{
      "sentence": "Grammatically correct English sentence from a unique real-world situation",
      "target_tense": "Target tense name"
    }}
  ]
}}

"""

def get_convert_tenses_evaluation_prompt(safe_target_tense, safe_sentence, safe_user_answer):
    return f"""
You are a strict English grammar evaluator.

TASK:
Evaluate whether the USER'S ANSWER correctly uses the TARGET TENSE.

TARGET TENSE:
"{safe_target_tense}"

ORIGINAL SENTENCE (meaning reference only):
"{safe_sentence}"

USER'S ANSWER:
"{safe_user_answer}"

EVALUATION RULES (STRICT):
1. Judge ONLY the USER'S ANSWER.
2. Check ONLY tense correctness and basic grammar.
3. Do NOT introduce new situations, times, or events.
4. Do NOT improve style or rewrite beyond tense correction.
5. Do NOT mention the original sentence in feedback.
6. Do NOT invent examples.

DECISION:
- If the USER'S ANSWER correctly uses the TARGET TENSE → is_correct = true
- Otherwise → is_correct = false

OUTPUT RULES:

IF is_correct = true:
- corrected_sentence MUST be EXACTLY the user's sentence.
- feedback: one short sentence saying why the tense is correct.

IF is_correct = false:
- corrected_sentence MUST be:
  • a single sentence
  • grammatically correct
  • written in the TARGET TENSE
  • based ONLY on the user's sentence
  • NO explanations, NO extra words, NO context
- feedback MUST:
  • mention the incorrect verb or verb form
  • briefly state what tense is required
  • be encouraging
  • NOT include example sentences

FORMAT:
Respond ONLY with valid JSON:

{{
  "is_correct": true or false,
  "corrected_sentence": "ONLY the corrected sentence. Nothing else.",
  "feedback": "Brief explanation limited to the user's sentence"
}}
"""