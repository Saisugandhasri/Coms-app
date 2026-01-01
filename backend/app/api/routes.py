# from fastapi import APIRouter
# from app.models.schemas import ContentRequest, ContentResponse
# from app.services.content_generator import generate_content
# from app.services.assessment_service import (
#     start_assessment,
#     save_answer,
#     submit_assessment
# )
# from app.models.schemas import (
#     StartAssessmentResponse,
#     SaveAnswerRequest,
#     SubmitAssessmentRequest,
#     SubmitAssessmentResponse
# )

# router = APIRouter(prefix="/generate", tags=["Content Generation"])
# router_1 = APIRouter(prefix="/assessment", tags=["Assessment"])

# @router.post("/", response_model=ContentResponse)
# async def generate(request: ContentRequest):
#     return generate_content(request.topic)

# @router_1.post("/start", response_model=StartAssessmentResponse)
# async def start(topic: ContentRequest):
#     return start_assessment(topic.topic)

# @router_1.post("/answer")
# async def answer(request: SaveAnswerRequest):
#     return save_answer(
#         request.assessment_id,
#         request.question_id,
#         request.selected_answer
#     )
# @router_1.post("/submit", response_model=SubmitAssessmentResponse)
# async def submit(request: SubmitAssessmentRequest):
#     return submit_assessment(
#         request.assessment_id,
#     )

from fastapi import APIRouter, HTTPException
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
