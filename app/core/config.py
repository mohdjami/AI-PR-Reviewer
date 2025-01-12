# app/core/config.py
from typing import Optional, List
from pydantic_settings import BaseSettings
from enum import Enum

class EnvironmentType(str, Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"

class Settings(BaseSettings):
    # Basic API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Code Review Agent"
    VERSION: str = "0.1.0"
    DESCRIPTION: str = "An AI-powered code review system"
    
    # Environment
    ENVIRONMENT: EnvironmentType = EnvironmentType.DEVELOPMENT
    DEBUG: bool = True
    
    # Server Settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # CORS Settings
    ALLOWED_ORIGINS: List[str] = ["*"]
    ALLOWED_METHODS: List[str] = ["*"]
    ALLOWED_HEADERS: List[str] = ["*"]
    
    # API Security
    SECRET_KEY: str = "your-secret-key-here"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # External Services
    GITHUB_API_TOKEN: Optional[str] = None
    GEMINI_API_KEY: Optional[str] = None

    # Logging Settings
    LOG_LEVEL: str = "DEBUG"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    LOG_FORMAT: str = "json"  # json or text
    LOG_FILE_PATH: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"  # This allows extra fields in the environment

# Create global settings instance
settings = Settings()