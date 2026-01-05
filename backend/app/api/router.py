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

from app.core.store import ASSESSMENTS

router = APIRouter(prefix="/assessment", tags=["Assessment"])

@router.post("/listening/start", response_model=StartListeningAssessmentResponse)
def start_listening():
    return start_listening_assessment()

@router.post("/submit", response_model=SubmitAssessmentResponse)
def submit_assessment(request: SubmitAssessmentRequest):
    assessment = ASSESSMENTS.get(request.assessment_id)
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    
    # Convert Pydantic model to dict for service compatibility
    # The services expect 'answers' to have specific structure, or we adapt here.
    # Current services:
    # submit_reading_assessment(id, answers: dict)
    # The services (Step 163, 172) iterate: for idx, q in enumerate... answers.get(idx)
    # But now answers is structured: answers.mcqs, answers.one_word
    
    # We need to adapt the answers or update services?
    # The user updated services in 163 and 172 to handle:
    # user_ans = answers["one_word"].get(str(idx), "")
    
    # BUT for MCQs:
    # if answers.get(idx) == mcq["correct_answer"]:
    # This expects answers to be flat OR answers["mcqs"]?
    
    # Let's check service code from user edits (Step 163/172).
    # Step 163 reading: 
    # for idx, mcq in enumerate(assessment["mcqs"]):
    #     if answers.get(idx) == mcq["correct_answer"]:
    # 
    # Step 172 listening: same.
    
    # This logic fails if passed `request.answers` which is an AssessmentAnswers object.
    # It also fails if passed a dict `{'mcqs':..., 'one_word':...}` because `answers.get(idx)` will fail for integer idx.
    
    # Code in 163/172:
    # for idx, q in enumerate(assessment["one_word_questions"]):
    #    user_ans = answers["one_word"].get(str(idx), "")
    
    # This implies `answers` is a dict with key "one_word".
    # But for MCQs it seemingly expects `answers` to direct access `answers.get(idx)`.
    # This is contradictory. The user likely copied old MCQ logic and added new one_word logic.
    
    # FIX: We should pass a normalized simple dict to services OR update services.
    # Updating services is cleaner. But let's look at router logic first.
    
    # I will modify the router to dispatch, but I also need to FIX the service logic 
    # because `answers.get(idx)` won't work if answers is `{'mcqs': {..}, 'one_word': {..}}`.
    
    # Let's flatten or route correctly?
    # No, services need to know about the structure.
    
    mode = assessment.get("mode")
    answers_dict = request.answers.model_dump() # {'mcqs': {..}, 'one_word': {..}}
    
    if mode == "reading":
        return submit_reading_assessment(request.assessment_id, answers_dict)
    elif mode == "listening":
        return submit_listening_assessment(request.assessment_id, answers_dict)
    
    raise HTTPException(status_code=400, detail="Invalid assessment mode")

# Compatibility / Legacy routes if needed? 
# The frontend uses /assessment/listening/start and /assessment/submit.
# What about reading start? Frontend Index.html uses /reading_comprehension/start AND /assessment/submit.
# Wait, user Step 180: const response = await fetch("http://localhost:8000/reading_comprehension/start"
# So we need to KEEP the reading start endpoint or redirect it.
# I will keep a specific endpoint for reading start.

@router.post("/reading/start", response_model=StartReadingAssessmentResponse)
def start_reading():
    return start_reading_assessment()