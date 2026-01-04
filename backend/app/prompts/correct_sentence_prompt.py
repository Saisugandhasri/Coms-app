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

SCENARIO DIVERSITY (CRITICAL — DO NOT IGNORE):
- Each sentence MUST come from a CLEARLY DIFFERENT real-world situation.
- Think broadly about real life: work, family, health, emotions, technology, weather,
  travel, education, shopping, social events, emergencies, hobbies, news, or personal goals etc....
- Do NOT reuse similar actions, subjects, or storylines.
- Do NOT generate multiple sentences that could happen on the same day or event.
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
   - incorrect pronoun case  Ex:(I vs me, he vs him)
   - Countable/uncountable noun confusion
   - Adjective vs adverb confusion Ex:(quick vs quickly)
   - Modal verb errors Ex:(can vs could, will vs would)
   - Conditional tense mistakes (if clauses)
4. Sentences MUST sound natural EXCEPT for the mistake.
5. Each sentence MUST be from a DIFFERENT real-life scenario.
6. Do NOT include explanations.
7. Do NOT include correct sentences.
8. Respond ONLY in valid JSON.


Response format (EXACT):

{{
  "questions": [
    {{
      "sentence": "Grammatically incorrect sentence here"
    }}
  ]
}}
"""

def get_correct_sentence_evaluation_prompt(original_sentence, user_answer):
    return f"""
You are an experienced and friendly English grammar teacher.

TASK:
The user was given a grammatically INCORRECT sentence and asked to correct it.

ORIGINAL SENTENCE (incorrect):
"{original_sentence}"

USER'S ANSWER:
"{user_answer}"

YOUR JOB:
1. Check if the user's sentence is grammatically correct.
2. Check if it correctly fixes the mistake in the original sentence.
3. Ignore wording differences if the grammar is correct.

DECISION RULE:
- If the user's sentence is grammatically correct → is_correct = true
- If it still contains a grammatical mistake → is_correct = false

IF THE ANSWER IS CORRECT:
- Clearly say it is correct.
- Briefly explain what was fixed.
- Set "corrected_sentence" EXACTLY equal to the user's sentence.

IF THE ANSWER IS INCORRECT:
- Quote the exact incorrect part from the user's sentence.
- Briefly explain why it is wrong.
- Provide a corrected, natural sentence.

IMPORTANT RULES:
- Do NOT criticize the learner.
- Do NOT lecture grammar rules.
- Base feedback ONLY on the user's answer.
- "corrected_sentence" must NEVER be empty.
- "is_correct" MUST be boolean.

Respond ONLY in valid JSON:

{{
  "is_correct": true or false,
  "corrected_sentence": "Correct full sentence here",
  "feedback": "Friendly explanation"
}}
"""