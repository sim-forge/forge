from fastapi import APIRouter
from ...core.schema.base import ResponseModel

router = APIRouter()

@router.get("/health", response_model=ResponseModel)
async def health_check():
    """Health check endpoint."""
    return ResponseModel(
        success=True,
        message="SimForge API is running",
        data={"status": "healthy"}
    )