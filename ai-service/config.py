"""
ANANYA-AI Configuration Settings
Privacy-first configuration for AI services
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings with privacy constraints."""
    
    # API Settings
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8002
    DEBUG: bool = False
    
    # CORS (Backend will proxy, but allow direct access for dev)
    ALLOWED_ORIGINS: list = ["http://localhost:3000", "http://localhost:5173"]
    
    # Bias Detection Thresholds
    COMPLEXITY_THRESHOLD_HIGH: float = 12.0  # Flesch-Kincaid grade level
    COMPLEXITY_THRESHOLD_MEDIUM: float = 8.0
    PACE_DEVIATION_THRESHOLD: float = 2.0  # Standard deviations
    CLARIFICATION_FREQUENCY_THRESHOLD: int = 3  # Requests per session
    
    # Adaptation Settings
    SIMPLIFICATION_LEVELS: int = 3  # Number of difficulty variants
    
    # Privacy Settings (CRITICAL)
    LOG_USER_IDENTIFIERS: bool = False  # MUST remain False
    STORE_RAW_CONTENT: bool = False  # MUST remain False
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
