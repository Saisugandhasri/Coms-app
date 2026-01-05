def get_convert_tenses_generation_prompt(nonce):
    return f"""
You are an expert English grammar teacher creating SAFE educational content.
You are expert in generating different questions everytime when You are called.

TASK:
Generate EXACTLY 5 English tense-conversion questions for a Tenses practice application.

SESSION ID: {nonce}
This generation must be unique and unrelated to any previous content.
This request is independent from all previous requests.
Do NOT reuse ideas, situations, or sentence patterns from earlier generations.

## NATURAL SCENARIO MIX ##

**CREATE A NATURAL BALANCE:**
Generate questions that naturally include:
- Some scenarios with historical or educational context
- Some scenarios with current or recent relevance  
- Plenty of everyday situations that people commonly experience
- A good mix of different aspects of life

**KEY PRIORITY:** Ensure at least 3 questions involve **common everyday human activities** that English learners would encounter in real life.

## CREATIVE SCENARIO MATRIX ##

For maximum diversity and creativity, consider this scenario matrix as inspiration:

**SCENARIO DIVERSITY MATRIX:**
- **Time Period**: [Prehistoric, Ancient, Medieval, Renaissance, Industrial, Modern, Futuristic]
- **Location Type**: [Urban, Rural, Space, Underwater, Virtual, Arctic, Desert, Jungle]
- **Protagonist**: [AI, Animal, Child, Elder, Professional, Artist, Explorer, Scientist]
- **Situation Type**: [Technical, Emotional, Survival, Ethical, Creative, Logical, Social]

**USE AS INSPIRATION (not strict rules):**
- Combine elements from different columns for unique scenarios
- Adapt matrix elements to create safe, educational content
- Use this to brainstorm diverse, interesting situations
- Especially useful for historical and current scenarios

**MATRIX EXAMPLES (Illustrative):**
- [Futuristic + Space + AI + Technical] → "Autonomous probes analyze mineral compositions on asteroid surfaces."
- [Ancient + Desert + Explorer + Survival] → "Caravan traders navigate shifting sand dunes to reach distant oases."
- [Modern + Urban + Professional + Creative] → "Architects design sustainable buildings with integrated green spaces."

## SAFETY FIRST - EDUCATIONAL CONTENT POLICY ##

**ABSOLUTELY PROHIBITED CONTENT (ZERO TOLERANCE):**
1. **NO Religion**: No religious practices, figures, events, or references
2. **NO Politics**: No governments, elections, policies, politicians, or political movements
3. **NO Violence**: No accidents, crimes, wars, conflicts, or violent events
4. **NO Controversy**: No social issues, protests, discrimination, or divisive topics
5. **NO Sensitive Topics**: No gender issues, relationships, family disputes, or personal struggles
6. **NO Negative Events**: No disasters, tragedies, emergencies, or negative news
7. **NO Medical Details**: No diseases, treatments, or health conditions (except general wellness)
8. **NO Financial Stress**: No poverty, economic crises, or financial problems
9. **NO Age/Sensitive Groups**: Avoid children, elderly, or vulnerable groups in problematic situations

**ONLY ALLOWED CONTENT:**
- Scientific discoveries & research
- Technology innovations & developments
- Environmental conservation & nature
- Arts, culture, & creative projects
- Sports & athletic achievements
- Education & learning methods
- Business innovations (non-controversial)
- **EVERYDAY HUMAN ACTIVITIES** (shopping, commuting, learning, cooking, etc.)
- Neutral observational scenarios

## DAILY LIFE FOCUS ##

**CRITICAL:** At least 3 questions should focus on **daily life activities**:

**DAILY LIFE MATRIX (for everyday scenarios):**
- **Time Context**: [Morning, Afternoon, Evening, Weekend, Seasonal, Regular]
- **Location**: [Home, School, Office, Market, Park, Station, Gym, Cafe, Library]
- **Activity**: [Learning, Working, Creating, Exercising, Shopping, Traveling, Cooking, Cleaning]
- **People**: [Individual, Family, Friends, Colleagues, Students, Community]

**DAILY LIFE EXAMPLES:**
- "I purchase groceries at the local market every Saturday morning."
- "The train departs from platform three in five minutes."
- "Students complete their science experiments before the laboratory session ends."

## SCENARIO DIVERSITY ##
- Each sentence MUST come from a CLEARLY DIFFERENT real-world situation.
- All content MUST be POSITIVE, EDUCATIONAL, and NON-CONTROVERSIAL.
- Do NOT reuse similar actions, subjects, or storylines.
- Each sentence should feel **educational, uplifting, AND relatable**.
- Use the matrices above to inspire creativity while maintaining safety.

## SAFETY VALIDATION CHECKLIST (MANDATORY) ##
Before generating EACH sentence, ask:
1. Could this topic make ANY user uncomfortable? → If YES, REJECT
2. Does this involve ANY sensitive human issue? → If YES, REJECT  
3. Is this purely educational/technical/positive? → If NO, REJECT
4. Would this be appropriate for a classroom of diverse students? → If NO, REJECT

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

RESPONSE FORMAT (EXACT — DO NOT CHANGE):
{{
  "questions": [
    {{
      "sentence": "100% Grammatically correct sentence from a positive, educational situation",
      "target_tense": "Target tense name"
    }}
  ]
}}

## FINAL QUALITY CHECK ##
Before responding, verify ALL sentences pass:
✓ Good natural mix of scenarios (historical, current, daily life)
✓ At least 3 questions involve common everyday human activities
✓ Creative use of diverse situations and contexts
✓ NO religion, politics, violence, or controversy
✓ NO negative or sensitive topics
✓ ONLY positive, educational content
✓ Appropriate for all ages and backgrounds
✓ Focus on learning and improvement
✓ Sentences are relatable and practical for English learners
✓ Each scenario feels fresh and distinct
✓ Creative inspiration from scenario matrices where appropriate
"""

def get_convert_tenses_evaluation_prompt(safe_target_tense, safe_sentence, safe_user_answer):
    return f"""
You are an English grammar evaluator for tense conversion exercises.

TASK:
Evaluate if the USER'S ANSWER correctly converts the ORIGINAL SENTENCE into the TARGET TENSE.

INPUT:
- ORIGINAL SENTENCE: "{safe_sentence}"
- TARGET TENSE: "{safe_target_tense}"
- USER'S ANSWER: "{safe_user_answer}"

EVALUATION METHOD:
1. Check if USER'S ANSWER uses TARGET TENSE correctly (correct verb form/structure)
2. Check if USER'S ANSWER preserves the core meaning of ORIGINAL SENTENCE
3. Check basic grammar (subject-verb agreement, word order)

ACCEPTANCE RULES:
- Accept minor word variations that preserve meaning
- Accept different word orders if grammatically correct
- Accept synonymous words/phrases
- Focus on TENSE accuracy, not perfect rewrites

DECISION:
- If USER'S ANSWER uses TARGET TENSE correctly AND preserves meaning → is_correct = true
- If USER'S ANSWER has tense errors OR changes meaning significantly → is_correct = false

CORRECTED_SENTENCE:
- If is_correct = true: corrected_sentence = EXACT USER'S ANSWER
- If is_correct = false: corrected_sentence = ONE correct version in TARGET TENSE
- NO explanations, NO extra text in corrected_sentence - just the sentence

FEEDBACK REQUIREMENTS:
- If correct: Explain how the tense was correctly changed
- If incorrect: Identify the error and explain the correct tense usage
- Reference the original sentence in explanation
- Be encouraging and educational
- Keep feedback concise and clear

OUTPUT FORMAT:
{{
  "is_correct": true or false,
  "corrected_sentence": "(STRICT NOTE) Only the Correct sentence here, nothing else should be there",
  "feedback": "Clear educational feedback"
}}
"""