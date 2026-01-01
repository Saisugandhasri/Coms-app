from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import router_image
app = FastAPI(title="Communication Application")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router_image)
