import uuid
from app.services.content_generator import generate_content
from app.core.store import ASSESSMENTS


def start_assessment(topic: str) -> dict:
    assessment_id = str(uuid.uuid4())
    content = generate_content(topic)

    ASSESSMENTS[assessment_id] = {
        "mcqs": content["mcqs"],
    }

    return {
        "assessment_id": assessment_id,
        "paragraph": content["paragraph"],
        "mcqs": content["mcqs"],
    }


def submit_assessment(assessment_id: str, answers: dict) -> dict | None:
    assessment = ASSESSMENTS.get(assessment_id)
    if not assessment:
        return None

    score = 0
    for idx, mcq in enumerate(assessment["mcqs"]):
        if answers.get(idx) == mcq["correct_answer"]:
            score += 1

    return {"score": score}
