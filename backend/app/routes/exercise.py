from fastapi import APIRouter, UploadFile, File, Form
from pydantic import BaseModel
from uuid import uuid4
from app.services.llm_service import generate_tense_question, evaluate_answer
from fastapi.responses import FileResponse
from app.services.tts_service import text_to_speech
import os


router = APIRouter(prefix="/api/exercise", tags=["Exercise"])


# -----------------------
# Schemas
# -----------------------
class AnswerRequest(BaseModel):
    exercise_id: str
    sentence: str
    user_answer: str


# -----------------------
# Routes
# -----------------------
@router.get("/")
def health():
    return {"status": "Exercise service running"}


@router.get("/tense")
def get_tense_exercise():
    """
    LLaMA generates the question
    """
    question = generate_tense_question()

    return {
        "exercise_id": str(uuid4()),
        "sentence": question["sentence"],
        "topic": question.get("topic", "tense")
    }


@router.post("/tense/answer/text")
def submit_text_answer(payload: AnswerRequest):
    """
    LLaMA evaluates text answer
    """
    result = evaluate_answer(
        sentence=payload.sentence,
        user_answer=payload.user_answer
    )

    return {
        "exercise_id": payload.exercise_id,
        **result
    }


@router.post("/tense/answer/audio")
def submit_audio_answer(
    exercise_id: str = Form(...),
    sentence: str = Form(...),
    audio_file: UploadFile = File(...)
):
    """
    Whisper → text → LLaMA
    """

    # TODO: Whisper transcription
    transcribed_text = "I went to the store yesterday"

    result = evaluate_answer(
        sentence=sentence,
        user_answer=transcribed_text
    )

    return {
        "exercise_id": exercise_id,
        **result
    }


from pydantic import BaseModel

class TTSRequest(BaseModel):
    text: str


@router.post("/tts")
def tts_endpoint(payload: TTSRequest):
    """
    Convert given text to speech and return audio file.
    """
    path = text_to_speech(payload.text)
    return FileResponse(
        path,
        media_type="audio/wav",
        filename=os.path.basename(path),
    )
