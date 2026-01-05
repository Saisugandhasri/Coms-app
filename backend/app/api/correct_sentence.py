from fastapi import APIRouter, UploadFile, File, Form
from pydantic import BaseModel
from uuid import uuid4
from fastapi.responses import FileResponse
import os
import shutil

from app.services.llm_service import generate_incorrect_sentence_batch, evaluate_correction
from app.services.coqui_Stts_service import text_to_speech
from app.services.stt_service import speech_to_text
from app.models.schemas import AnswerRequest_Correct, TTSRequest

router = APIRouter(prefix="/api/exercise", tags=["Correct Sentence"])


# -----------------------
# Schemas
# -----------------------




# -----------------------
# Routes
# -----------------------
@router.get("/")
def health():
    return {"status": "Exercise service running"}


@router.post("/correct/start")
def start_correct_sentence_exercise():
    data = generate_incorrect_sentence_batch()

    return {
        "exercise_id": str(uuid4()),
        "questions": data["questions"]
    }



@router.post("/correct/answer/text")
def submit_text_answer(payload: AnswerRequest_Correct):
    """
    LLaMA evaluates text answer
    """
    result = evaluate_correction(
        original_sentence=payload.sentence,
        user_answer=payload.user_answer,
    )

    return {
        "exercise_id": payload.exercise_id,
        **result,
    }


@router.post("/correct/answer/audio")
async def submit_audio_answer(
    exercise_id: str = Form(...),
    sentence: str = Form(...),
    audio_file: UploadFile = File(...),
):
    """
    Whisper → text → LLaMA
    """

    # 1. Save uploaded audio to disk
    os.makedirs("../../temp_audio", exist_ok=True)
    audio_path = f"temp_audio/{uuid4()}_{audio_file.filename}"

    with open(audio_path, "wb") as buffer:
        shutil.copyfileobj(audio_file.file, buffer)

    # 2. Speech to text (Whisper expects FILE PATH)
    transcribed_text = speech_to_text(audio_path)

    # 3. Cleanup temp file
    os.remove(audio_path)

    # 4. Evaluate with LLM
    result = evaluate_correction(
        original_sentence=sentence,
        user_answer=transcribed_text,
    )

    return {
        "exercise_id": exercise_id,
        "transcribed_text": transcribed_text,
        **result,
    }




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
