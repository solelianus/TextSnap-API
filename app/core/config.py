from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from pathlib import Path
from typing import Optional

class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "TextSnap API"
    
    # Server Settings
    HOST: str = "0.0.0.0"
    PORT: int = 8080
    RELOAD: bool = False
    
    # Path Settings
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    FONTS_DIR: Path = BASE_DIR / "assets" / "fonts"
    OUTPUT_DIR: Path = BASE_DIR / "output"
    CACHE_DIR: Path = BASE_DIR / "cache"
    LOGS_DIR: Path = BASE_DIR / "logs"
    
    # Database Settings
    DB_FILE: str = "fonts.db"
    
    # Security
    SECRET_KEY: str = "your-secret-key-here"  # Change in production
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # Image Processing
    MAX_IMAGE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_IMAGE_FORMATS: list = ["png", "jpg", "jpeg", "webp"]
    ALLOWED_OUTPUT_FORMATS: list = ["png", "jpg", "jpeg", "webp", "pdf"]
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    model_config = ConfigDict(
        case_sensitive=True,
        env_file=".env"
    )

settings = Settings() 