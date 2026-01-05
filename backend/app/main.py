
from app.api.exercise import router as exercise_router
from app.api.correct_sentence import router as correct_sentence_router


app.include_router(exercise_router)
app.include_router(correct_sentence_router)