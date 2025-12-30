from fastapi import APIRouter
from app.models.schemas import ContentRequest, ContentResponse
from app.services.content_generator import generate_content

router = APIRouter(prefix="/generate", tags=["Content Generation"])

@router.post("/", response_model=ContentResponse)
async def generate(request: ContentRequest):
    return generate_content(request.topic)
