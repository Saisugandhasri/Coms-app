from pydantic import BaseModel
from typing import List

class ContentRequest(BaseModel):
    topic: str

class MCQ(BaseModel):
    question: str
    options: List[str]
    correct_answer: str

class ContentResponse(BaseModel):
    paragraph: str
    mcqs: List[MCQ]

class Question(BaseModel):
    question_id: str
    question: str
    options: List[str]

class StartAssessmentResponse(BaseModel):
    assessment_id: str
    paragraph: str
    questions: List[Question]

class SaveAnswerRequest(BaseModel):
    assessment_id: str
    question_id: str
    selected_answer: str

class SubmitAssessmentRequest(BaseModel):
    assessment_id: str

class QuestionResult(BaseModel):
    question_id: str
    selected_answer: str
    correct_answer: str
    is_correct: bool

class SubmitAssessmentResponse(BaseModel):
    score: int

