import uuid
from app.services.content_generator import generate_content
from app.core.store import ASSESSMENTS,get_random_topic


def start_reading_assessment() -> dict:
    assessment_id = str(uuid.uuid4())
    topic = get_random_topic()
    content = generate_content(topic)
    # print(content)

    ASSESSMENTS[assessment_id] = {
        "mode" : "reading",
        "mcqs": content["mcqs"],
    }

    return {
        "assessment_id": assessment_id,
        "topic": topic,
        "paragraph": content["paragraph"],
        "mcqs": content["mcqs"],
    }


def submit_reading_assessment(assessment_id: str, answers: dict) -> dict | None:
    assessment = ASSESSMENTS.get(assessment_id)
    if not assessment:
        return None

    score = 0
    for idx, mcq in enumerate(assessment["mcqs"]):
        if answers.get(idx) == mcq["correct_answer"]:
            score += 1

    return {"score": score}
