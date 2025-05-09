import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    """Application settings."""
    APP_NAME: str = "SimForge"
    API_V1_PREFIX: str = "/api/v1"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_PATH: str = os.getenv("LOG_PATH", "../../logs/simforge.log")
    
    # LLM Settings
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "openai")
    LLM_API_KEY: str = os.getenv("LLM_API_KEY", "")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "gpt-4o")
    LOCAL_LLM_URL: str = os.getenv("LOCAL_LLM_URL", "http://localhost:11434")
    
    # Data Storage
    DATA_DIR: str = os.getenv("DATA_DIR", "../../data")
    SCHEMAS_DIR: str = os.getenv("SCHEMAS_DIR", "../../data/schemas")
    PROMPTS_DIR: str = os.getenv("PROMPTS_DIR", "../../data/prompts")
    SEQUENCES_DIR: str = os.getenv("SEQUENCES_DIR", "../../data/sequences")
    
    # Server Settings
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "12000"))
    
    class Config:
        env_file = "../configs/env/dev.env"
        case_sensitive = True
        extra = "ignore"

settings = Settings()