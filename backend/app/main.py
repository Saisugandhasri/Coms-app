from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import router_image,router_reading_com,router_listening_com
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Communication Application")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router_image)
app.include_router(router_reading_com)
app.include_router(router_listening_com)



app.mount("/audio", StaticFiles(directory="generated_audio"), name="audio")

@app.get("/health")
def health_check():
    return {"status": "Backend running"}
