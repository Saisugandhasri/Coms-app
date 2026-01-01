from pydantic import BaseModel
from typing import List, Dict


class StartAssessmentRequest(BaseModel):
    topic: str


class StartAssessmentResponse(BaseModel):
    assessment_id: str
    paragraph: str
    mcqs: List[Dict]


class SubmitAssessmentRequest(BaseModel):
    assessment_id: str
    answers: Dict[int, str]


class SubmitAssessmentResponse(BaseModel):
    score: int
