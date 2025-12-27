from fastapi import APIRouter, UploadFile, File ,Form
from pydantic import BaseModel
from uuid import uuid4

router = APIRouter()

# -----------------------
# Request Schemas
# -----------------------
class TextAnswerRequest(BaseModel):
    exercise_id: str
    user_answer: str


# -----------------------
# Routes
# -----------------------
@router.get("/")
def root():
    return {"status": "Backend is running"}

@router.get("/tense")
def get_tense_exercise():
    exercise_id = str(uuid4())

    return {
        "exercise_id": exercise_id,
        "sentence_text": "I go to the store yesterday",
        "audio_url": f"http://localhost:8000/audio/{exercise_id}.mp3"
    }

@router.post("/tense/answer/text")
def submit_text_answer(payload: TextAnswerRequest):
    correct_answer = "I went to the store yesterday"
    is_correct = payload.user_answer.strip().lower() == correct_answer.lower()

    return {
        "exercise_id": payload.exercise_id,
        "original_sentence": "I go to the store yesterday",
        "user_answer": payload.user_answer,
        "is_correct": is_correct,
        "mistakes": [] if is_correct else ["Verb tense incorrect"],
        "corrected_sentence": correct_answer,
        "feedback": "Dummy feedback (LLM later)"
    }


@router.post("/tense/answer/audio")
def submit_audio_answer(
    exercise_id: str = Form(...),
    audio_file: UploadFile = File(...)
):
    converted_text = "I went to the store yesterday"

    return {
        "exercise_id": exercise_id,
        "original_sentence": "I go to the store yesterday",
        "user_answer": converted_text,
        "is_correct": True,
        "mistakes": [],
        "corrected_sentence": converted_text,
        "feedback": "Dummy feedback from audio"
    }


@router.get("/audio/{exercise_id}.mp3")
def get_audio(exercise_id: str):
    return {"message": "Audio generation not implemented yet"}
