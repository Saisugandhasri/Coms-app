from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router,router_1

app = FastAPI(title="LLM Paragraph & MCQ Generator")

app.include_router(router)
app.include_router(router_1)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow frontend access
    allow_credentials=True,
    allow_methods=["*"],   # allows OPTIONS, POST, GET
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {"status": "Backend running"}