from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import router_image
from app.api.routes import router

app = FastAPI(title="Communication Application")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router_image)
app.include_router(router)


@app.get("/health")
def health_check():
    return {"status": "Backend running"}
