import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from app.api import api_router
from app.core.utils.config import settings
from app.core.utils.logger import app_logger

def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title=settings.APP_NAME,
        description="A local-first, production-grade synthetic cognition tool",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )
    
    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, this should be restricted
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include API routes
    app.include_router(api_router, prefix=settings.API_V1_PREFIX)
    
    @app.get("/")
    async def root():
        """Redirect to API documentation."""
        return RedirectResponse(url="/docs")
    
    @app.on_event("startup")
    async def startup_event():
        app_logger.info(f"Starting {settings.APP_NAME} API")
        app_logger.info(f"API documentation available at http://{settings.HOST}:{settings.PORT}/docs")
        app_logger.info(f"LLM provider: {settings.LLM_PROVIDER}, model: {settings.LLM_MODEL}")
    
    @app.on_event("shutdown")
    async def shutdown_event():
        app_logger.info(f"Shutting down {settings.APP_NAME} API")
    
    return app

app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
    )