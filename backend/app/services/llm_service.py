# llm_service.py
import os
import json
import re
from uuid import uuid4
from app.prompts.convert_tenses_prompt import get_convert_tenses_generation_prompt,get_convert_tenses_evaluation_prompt
from app.prompts.correct_sentence_prompt import get_correct_sentence_generation_prompt,get_correct_sentence_evaluation_prompt
from app.core.llm_client_cc import call_groq_api


# ---------------------------
# HELPER FUNCTION TO CALL GROQ SDK
# ---------------------------



# ---------------------------
# JSON EXTRACTION
# ---------------------------
def extract_json(text: str):
    """
    Safely extract JSON from LLM output
    """
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # Non-greedy match to avoid broken JSON
        match = re.search(r"\{[\s\S]*?\}", text)
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError:
                pass
        raise ValueError("LLM did not return valid JSON")


# -------------------------------------------------
# QUESTION GENERATION
# -------------------------------------------------
def generate_tense_questions_batch():
    """
    Generate EXACTLY 5 tense-conversion questions.
    Each sentence is grammatically correct and must NOT already be in the target tense.
    """
    nonce = uuid4().hex

    prompt = get_convert_tenses_generation_prompt(nonce)

    content = call_groq_api(prompt, temperature=0.7)
    parsed = extract_json(content)

    # ✅ HARD VALIDATION
    questions = parsed.get("questions", [])

    if len(questions) != 5:
        raise ValueError("LLM must return exactly 5 questions")

    seen_targets = set()
    for q in questions:
        if "sentence" not in q or "target_tense" not in q:
            raise ValueError("Invalid question format")
        if q["target_tense"] in seen_targets:
            raise ValueError("Duplicate target tense detected")
        seen_targets.add(q["target_tense"])

    return parsed



# -------------------------------------------------
# ANSWER EVALUATION
# -------------------------------------------------
def evaluate_answer(sentence: str, target_tense: str, user_answer: str):
    """
    Evaluate whether the user correctly converted the sentence
    into the given target tense.
    """

    # Escape braces to avoid f-string issues
    safe_sentence = sentence.replace("{", "{{").replace("}", "}}")
    safe_target_tense = target_tense.replace("{", "{{").replace("}", "}}")
    safe_user_answer = user_answer.replace("{", "{{").replace("}", "}}")

    prompt = get_convert_tenses_evaluation_prompt(safe_target_tense, safe_sentence, safe_user_answer)

    content = call_groq_api(prompt)
    result = extract_json(content)

    # ---------------------------
    # SAFETY NORMALIZATION
    # ---------------------------
    result["is_correct"] = bool(result.get("is_correct", False))
    if not result.get("corrected_sentence"):
        result["corrected_sentence"] = user_answer
    if not result.get("feedback"):
        result["feedback"] = "Please review the tense usage and try again."

    return result





def generate_incorrect_sentence_batch():
    """
    Generate EXACTLY 5 Grammatically incorrect sentences.
    """
    nonce = uuid4().hex

    prompt = get_correct_sentence_generation_prompt(nonce)

    content = call_groq_api(prompt, temperature=0.7)
    parsed = extract_json(content)

    # ✅ HARD VALIDATION
    questions = parsed.get("questions", [])

    if len(questions) != 5:
        raise ValueError("LLM must return exactly 5 questions")

    for q in questions:
        if "sentence" not in q:
            raise ValueError("Invalid question format")

    return parsed





def evaluate_correction(original_sentence: str, user_answer: str):
    """
    Evaluate whether the user correctly corrected the sentence.
    """

    prompt = get_correct_sentence_evaluation_prompt(original_sentence, user_answer)

    content = call_groq_api(prompt)
    result = extract_json(content)

    result["is_correct"] = bool(result.get("is_correct", False))
    if not result.get("corrected_sentence"):
        result["corrected_sentence"] = user_answer

    return result
