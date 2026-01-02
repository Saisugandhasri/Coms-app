from pydantic import BaseModel
from typing import List, Dict


class StartReadingAssessmentResponse(BaseModel):
    assessment_id: str
    topic: str
    paragraph: str
    mcqs: List[Dict]

class StartListeningAssessmentResponse(BaseModel):
    assessment_id: str
    topic: str
    audio_url:str
    mcqs: List[Dict]


class SubmitAssessmentRequest(BaseModel):
    assessment_id: str
    answers: Dict[int, str]


class SubmitAssessmentResponse(BaseModel):
    score: int
