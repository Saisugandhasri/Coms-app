from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.exercise import router as exercise_router
from app.api.correct_sentence import router as correct_sentence_router
app = FastAPI(title = "Convert the Tenses")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(exercise_router)
app.include_router(correct_sentence_router)