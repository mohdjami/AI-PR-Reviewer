# app/api/routes/health.py
from fastapi import APIRouter
from app.core.config import settings

router = APIRouter(
    prefix="/health",
    tags=["health"]
)

@router.get("/")
async def health_check():
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
        "version": settings.VERSION,
        "app_name": settings.PROJECT_NAME
    }