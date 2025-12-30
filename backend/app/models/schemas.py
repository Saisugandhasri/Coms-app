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