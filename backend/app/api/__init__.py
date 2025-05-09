from fastapi import APIRouter
from .routes import health, generation, fork, schemas, prompts

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(generation.router, prefix="/cognition", tags=["cognition"])
api_router.include_router(fork.router, prefix="/cognition", tags=["cognition"])
api_router.include_router(schemas.router, prefix="/schemas", tags=["schemas"])
api_router.include_router(prompts.router, prefix="/prompts", tags=["prompts"])