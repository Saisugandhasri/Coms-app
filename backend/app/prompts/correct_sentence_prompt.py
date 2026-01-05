def get_correct_sentence_generation_prompt(nonce):
    return f"""
You are an expert English grammar teacher.
You are expert in generating different questions everytime when You are called.

TASK:(SOUL OF APPLICATION)
Generate EXACTLY 5 English sentences that are grammatically INCORRECT, this Incorrectness can be choose from below given list.

SESSION ID: {nonce}
This generation must be unique and unrelated to any previous content.
This request is independent from all previous requests.
Do NOT reuse ideas, situations, or sentence patterns from earlier generations.

## SAFETY FILTERS (STRICT) ##
- No religion, politics, or controversial topics
- No violence, accidents, or negative events  
- No sensitive personal or social issues
- No medical/financial distress topics
- No problematic depictions of age/sensitive groups
- Keep all content positive, educational, and universally appropriate

## SCENARIO DIVERSITY SYSTEM ##

1. SCENARIO SOURCES (Mix from these categories):

   A. **POSITIVE CURRENT AFFAIRS** (Include 1-2 questions):
      - Scientific research breakthroughs
      - Technology innovations (AI, robotics, software)
      - Environmental conservation progress
      - Space/astronomy discoveries
      - Cultural/arts achievements (movies, music, art)
      - Sports records/achievements
      - Educational advancements
      - Positive community initiatives

   B. **SCENARIO MATRIX** (Use for 2-3 questions):
      - Time Period: [Prehistoric, Ancient, Medieval, Renaissance, Industrial, Modern, Futuristic]
      - Location Type: [Urban, Rural, Space, Underwater, Virtual, Arctic, Desert, Jungle]
      - Protagonist: [AI, Animal, Child, Elder, Professional, Artist, Explorer, Scientist]
      - Situation Type: [Technical, Emotional, Survival, Ethical, Creative, Logical, Social]

   C. **DAILY LIFE CATEGORIES** (Use for remaining questions):
      - work, family, health, emotions, technology, weather, travel, education, 
        shopping, social events, emergencies, hobbies, news, personal goals

2. DISTRIBUTION: Mix 1-2 current affairs, 2-3 matrix scenarios, rest daily life

SCENARIO DIVERSITY (CRITICAL — DO NOT IGNORE):
- Each sentence MUST come from a CLEARLY DIFFERENT real-world situation.
- Use the mixed sources above to ensure maximum diversity.
- Do NOT reuse similar actions, subjects, or storylines.
- Do NOT generate multiple sentences that could happen in the same day or event.
- Each sentence should feel like it belongs to a completely different story.
- Be creative, realistic, and natural.

STRICT RULES:
1. Each sentence MUST be clearly wrong.
2. Each sentence MUST contain ONLY ONE main grammatical mistake.
3. Mistakes may include:
   - wrong tense
   - subject–verb agreement
   - incorrect verb form
   - incorrect article usage
   - incorrect preposition
   - incorrect pronoun case (I vs me, he vs him)
   - Countable/uncountable noun confusion
   - Adjective vs adverb confusion (quick vs quickly)
   - Modal verb errors (can vs could, will vs would)
   - Conditional tense mistakes (if clauses)
4. Sentences MUST sound natural EXCEPT for the mistake.
5. Each sentence MUST be from a DIFFERENT real-life scenario.
6. Do NOT include explanations.
7. Do NOT include correct sentences.
8. Respond ONLY in valid JSON.

## ERROR DISTRIBUTION GUIDELINES ##
- Use DIFFERENT mistake types across the 5 sentences
- Ensure each error is clearly identifiable
- Make errors realistic (common ESL mistakes)
- Avoid overly complex or ambiguous errors

RESPONSE FORMAT (EXACT):
{{
  "questions": [
    {{
      "sentence": "Grammatically incorrect sentence here"
    }}
  ]
}}

## QUALITY CHECK ##
Before responding, verify:
✓ 5 completely different scenarios (mix of current affairs, matrix, daily life)
✓ Each sentence has only ONE clear grammatical error
✓ Different error types across sentences
✓ Sentences sound natural except for the intentional error
✓ No repetition in themes or situations
✓ All content is safe, positive, and educational
"""

def get_correct_sentence_evaluation_prompt(original_sentence, user_answer):
    return f"""
You are a friendly English grammar teacher evaluating "Correct the Sentence" exercises.

TASK:
Evaluate if the USER'S ANSWER correctly fixes the grammatical error in the ORIGINAL SENTENCE.

ORIGINAL SENTENCE (incorrect):
"{original_sentence}"

USER'S ANSWER:
"{user_answer}"

EVALUATION FOCUS:
1. Is USER'S ANSWER grammatically correct?
2. Does it fix the specific error in ORIGINAL SENTENCE?
3. Ignore wording variations if grammar is correct

DECISION:
- If USER'S ANSWER is grammatically correct AND fixes the original error → is_correct = true
- If USER'S ANSWER has any grammatical error OR doesn't fix the original error → is_correct = false

CORRECTED_SENTENCE:
- If correct: Use USER'S EXACT ANSWER
- If incorrect: Provide ONE correct version
- Sentence only - no explanations

FEEDBACK REQUIREMENTS:

IF CORRECT:
1. Confirm it's correct
2. Identify the error type that was fixed (e.g., "subject-verb agreement error", "incorrect article usage")
3. Explain what was corrected
4. Be encouraging

IF INCORRECT:
1. Identify the error type in user's answer
2. Quote the incorrect part
3. Explain why it's wrong
4. Provide the correct grammar rule
5. Be supportive and encouraging
6. Identify the error type (same categories as generation)

COMMON ERROR TYPES TO IDENTIFY:
- Wrong tense
- Subject-verb agreement error
- Incorrect verb form
- Incorrect article usage (a/an/the)
- Incorrect preposition
- Pronoun case error (I/me, he/him)
- Countable/uncountable noun confusion
- Adjective/adverb confusion
- Modal verb error
- Conditional tense mistake

EXAMPLE FEEDBACK STRUCTURE:

For correct answer:
"Perfect! You correctly fixed the subject-verb agreement error. 'The team are working' becomes 'The team is working' - singular subject needs singular verb."

For incorrect answer:
"Good attempt! You still have a preposition error. 'Dependent from' should be 'dependent on'. Remember: we use 'on' with 'dependent' to show reliance. Try again with 'dependent on'."

OUTPUT FORMAT (STRICT JSON):
{{
  "is_correct": true or false,
  "corrected_sentence": "(STRICT NOTE) Only the Correct sentence here, nothing else should be there",
  "feedback": "Friendly explanation with error type identification"
}}

BE FRIENDLY & ENCOURAGING:
- Always start positively
- Focus on learning, not mistakes
- Use supportive language
- Build confidence
"""