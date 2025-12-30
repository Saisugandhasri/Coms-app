# import uuid
# from app.services.content_generator import generate_content
# from app.core.store import ASSESSMENTS

# def start_assessment(topic: str):
#     content = generate_content(topic)
#     assessment_id = str(uuid.uuid4())
#     correct_answers = {}
#     user_answers = {}
#     questions = []

#     for idx,mcq in enumerate(content["mcqs"]):
#         qid = f"q{idx+1}"
#         correct_answers[qid] = mcq.get("correct_answer")

#         if mcq.get("correct_answer") is None:
#             continue

#         questions.append({
#             "question_id": qid,
#             "question": mcq["question"],
#             "options": mcq["options"],
#         })
#     ASSESSMENTS[assessment_id] = {
#         "correct_answer": correct_answers,
#         "user_answer" : user_answers
#     }

#     return{
#         "assessment_id": assessment_id,
#         "paragraph" : content["paragraph"],
#         "questions": questions,
#     }

# def save_answer(assessment_id, question_id, selected_answer):
#     assessment = ASSESSMENTS[assessment_id]

#     if not assessment:
#         raise ValueError("assessment not found")
#     if "user_answer" not in assessment:
#         assessment["user_answer"] = {}
#     assessment["user_answers"][question_id] = selected_answer
#     return {"status":"saved"}

# def submit_assessment(assessment_id: str):
#     assessment = ASSESSMENTS.get(assessment_id)

#     if not assessment:
#         raise ValueError("Invalid assessment ID")

#     score = 0
#     for qid, correct_answer in assessment["correct_answers"].items():
#         selected = assessment["user_answers"].get(qid)
#         is_correct = selected == correct_answer

#         if is_correct:
#             score += 1

#     return {
#         "score": score,
#     }
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
