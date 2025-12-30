from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="LLM Paragraph & MCQ Generator")

app.include_router(router)

@app.get("/")
def health_check():
    return {"status": "Backend running"}