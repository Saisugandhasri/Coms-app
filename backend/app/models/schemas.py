from pydantic import BaseModel
from typing import List, Dict



class OneWordQuestion(BaseModel):
    question: str
    answer: str

class StartReadingAssessmentResponse(BaseModel):
    assessment_id: str
    topic: str
    paragraph: str
    mcqs: List[Dict]
    one_word_questions: List[OneWordQuestion]

class StartListeningAssessmentResponse(BaseModel):
    assessment_id: str
    topic: str
    audio_url:str
    max_replays: int
    mcqs: List[Dict]
    one_word_questions: List[OneWordQuestion]


class AssessmentAnswers(BaseModel):
    mcqs: Dict[str, str]
    one_word: Dict[str, str]

class SubmitAssessmentRequest(BaseModel):
    assessment_id: str
    answers: AssessmentAnswers


class SubmitAssessmentResponse(BaseModel):
    score: int
    correct_answers: Dict[str, Dict[str, str]]
