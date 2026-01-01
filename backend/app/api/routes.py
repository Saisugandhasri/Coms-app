from fastapi import APIRouter, HTTPException, UploadFile, File
from app.models.schemas import (
    StartAssessmentRequest,
    StartAssessmentResponse,
    SubmitAssessmentRequest,
    SubmitAssessmentResponse,
)
from app.services.assessment_service import (
    start_assessment,
    submit_assessment,
)





router = APIRouter(prefix="/assessment", tags=["Assessment"])


@router.post("/start", response_model=StartAssessmentResponse)
def start(request: StartAssessmentRequest):
    return start_assessment(request.topic)


@router.post("/submit", response_model=SubmitAssessmentResponse)
def submit(request: SubmitAssessmentRequest):
    result = submit_assessment(
        request.assessment_id,
        request.answers,
    )
    if not result:
        raise HTTPException(status_code=404, detail="Assessment not found")
    return result
