from app.api.router import router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles 
app = FastAPI(title="Communication Application")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router)



app.mount("/audio", StaticFiles(directory="generated_audio"), name="audio")

@app.get("/health")
def health_check():
    return {"status": "Backend running"}
