from typing import Optional
from pydantic import BaseSettings
from enum import Enum

class Environment(str, Enum):
    DEVELOPMENT = "development"
    TESTING = "testing"
    STAGING = "staging"
    PRODUCTION = "production"

class Settings(BaseSettings):
    #Basic API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Code Review Agent" 
    DESCRIPTION: str = "An AI-powered code review system"
    VERSION: str = "0.1.0"

    #Environment Settings
    ENVIRONMENT: Environment = Environment.DEVELOPMENT
    DATABASE_URL: Optional[str] = None
    DEBUG: bool = True

    class Config:
        env_file = ".env"
    
    #Server Settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    #CORS Settings
    ALLOWED_ORIGINS: list[str] = ["*"]
    ALLOWED_METHODS: list[str] = ["*"]
    ALLOWED_HEADERS: list[str] = ["*"]

    #API Security Settings
    SECRET_KEY: str = "d3a6f7d3c9b3c6e7b1c6a7d3f6b3c9b3"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    GITHUB_API_TOKEN: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None

settings = Settings()