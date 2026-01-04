import uuid
from app.core.store import ASSESSMENTS, get_random_topic
from app.services.content_generator import generate_content
from app.services.tts_service import generate_audio

def start_listening_assessment() -> dict:
    assessment_id = str(uuid.uuid4())
    topic = get_random_topic()

    content = generate_content(topic)
    print(content)
    audio_id = generate_audio(content["paragraph"])

    ASSESSMENTS[assessment_id] = {
        "mode": "listening",
        "mcqs": content["mcqs"],
        "one_word_questions": content["one_word_questions"],

    }

    return {
        "assessment_id": assessment_id,
        "topic": topic,
        "audio_url": f"http://localhost:8000/audio/{audio_id}",
        "max_replays": 3,
        "mcqs": content["mcqs"],
        "one_word_questions": content["one_word_questions"],
    }

def submit_listening_assessment(assessment_id: str, answers: dict) -> dict | None:
    assessment = ASSESSMENTS.get(assessment_id)
    if not assessment:
        return None

    score = 0
    # Answers is now {'mcqs': {...}, 'one_word': {...}}
    mcq_answers = answers.get("mcqs", {})
    one_word_answers = answers.get("one_word", {})

    correct_answers = {
        "mcqs": {},
        "one_word": {}
    }

    for idx, mcq in enumerate(assessment["mcqs"]):
        correct_answers["mcqs"][str(idx)] = mcq["correct_answer"]
        if mcq_answers.get(str(idx)) == mcq["correct_answer"]:
            score += 1
    
    for idx, q in enumerate(assessment["one_word_questions"]):
        correct_answers["one_word"][str(idx)] = q["answer"]
        user_ans = one_word_answers.get(str(idx), "").lower().strip()
        correct_ans = q["answer"].lower().strip()
        if user_ans == correct_ans:
            score += 1

    return {"score": score, "correct_answers": correct_answers}