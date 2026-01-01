from fastapi import APIRouter, HTTPException, UploadFile, File










from services.whisper_service import transcribe_audio_from_bytes
from services.utils import calculate_wpm, count_fillers
from services.feedback_service import evaluate_speech
from services.relevance_service import check_relevance


router_image= APIRouter()
















@router_image.post("/process-audio")
async def process_audio(file: UploadFile = File(...), duration: float = 0):

    audio_bytes = await file.read()

    transcript, audio_id = transcribe_audio_from_bytes(audio_bytes)


    evaluation = evaluate_speech(transcript, wpm)
    relevance = check_relevance(transcript)

    return {
        "audio_id": audio_id,
        "transcript": transcript,
        "wpm": wpm,
        "filler_word_count": filler_count,
        "evaluation": evaluation,
        "relevance": relevance
    }