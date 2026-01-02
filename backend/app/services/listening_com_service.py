import uuid
from app.core.store import ASSESSMENTS, get_random_topic
from app.services.content_generator import generate_content
from app.services.tts_service import generate_audio

def start_listening_assessment() -> dict:
    assessment_id = str(uuid.uuid4())
    topic = get_random_topic()

    content = generate_content(topic)
    audio_id = generate_audio(content["paragraph"])

    ASSESSMENTS[assessment_id] = {
        "mode": "listening",
        "mcqs": content["mcqs"],
    }

    return {
        "assessment_id": assessment_id,
        "topic": topic,
        "audio_url": f"http://localhost:8000/audio/{audio_id}",
        "mcqs": content["mcqs"],
    }

def submit_listening_assessment(assessment_id: str, answers: dict) -> dict | None:
    assessment = ASSESSMENTS.get(assessment_id)
    if not assessment:
        return None

    score = 0
    for idx, mcq in enumerate(assessment["mcqs"]):
        if answers.get(idx) == mcq["correct_answer"]:
            score += 1

    return {"score": score}