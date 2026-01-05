class AnswerRequest_Convert(BaseModel):
    exercise_id: str
    sentence: str
    target_tense: str
    user_answer: str



class TTSRequest(BaseModel):
    text: str


class AnswerRequest_Correct(BaseModel):
    exercise_id: str
    sentence: str
    user_answer: str
