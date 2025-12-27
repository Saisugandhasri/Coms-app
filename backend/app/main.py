from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.tense import router as tense_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tense_router, prefix="/api/exercise")
