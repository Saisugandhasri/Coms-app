from fastapi import APIRouter, HTTPException, UploadFile, File
from app.models.schemas import (
    StartReadingAssessmentResponse,
    StartListeningAssessmentResponse,
    SubmitAssessmentRequest,
    SubmitAssessmentResponse,
)
from app.services.reading_com_service import (
    start_reading_assessment,
    submit_reading_assessment,
)
from app.services.listening_com_service import (
    start_listening_assessment,
    submit_listening_assessment
)
from app.services.whisper_service import transcribe_audio_from_bytes
from app.services.utils import calculate_wpm, count_fillers
from app.services.feedback_service import evaluate_speech
from app.services.relevance_service import check_relevance
from app.services.listening_com_service import start_listening_assessment

router_reading_com = APIRouter(prefix="/reading_comprehension", tags=["Reading_Comprehension"])
router_listening_com = APIRouter(prefix="/listening_comprehension", tags=["Listening_Comprehension"])

router_image= APIRouter()

@router_listening_com.post("/start", response_model=StartListeningAssessmentResponse)
def start():
    return start_listening_assessment()

@router_listening_com.post("/submit", response_model=SubmitAssessmentResponse)
def submit(request: SubmitAssessmentRequest):
    result = submit_listening_assessment(
        request.assessment_id,
        request.answers,
    )
    if not result:
        raise HTTPException(status_code=404, detail="Assessment not found")
    return result

@router_reading_com.post("/start", response_model=StartReadingAssessmentResponse)
def start():
    return start_reading_assessment()


@router_reading_com.post("/submit", response_model=SubmitAssessmentResponse)
def submit(request: SubmitAssessmentRequest):
    result = submit_reading_assessment(
        request.assessment_id,
        request.answers,
    )
    if not result:
        raise HTTPException(status_code=404, detail="Assessment not found")
    return result



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