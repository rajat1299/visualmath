from pydantic_settings import BaseSettings
import os
from typing import List, Dict
from datetime import datetime, timedelta

class APIKey:
    def __init__(self, key: str, rate_limit: int, expires_at: datetime = None):
        self.key = key
        self.rate_limit = rate_limit  # requests per minute
        self.expires_at = expires_at
        self.last_used = None
        self.request_count = 0

    def is_valid(self) -> bool:
        if self.expires_at and datetime.utcnow() > self.expires_at:
            return False
        return True

    def can_make_request(self) -> bool:
        now = datetime.utcnow()
        if not self.last_used:
            self.last_used = now
            self.request_count = 1
            return True
        
        # Reset counter if minute has passed
        if (now - self.last_used) > timedelta(minutes=1):
            self.request_count = 0
            self.last_used = now
        
        if self.request_count >= self.rate_limit:
            return False
        
        self.request_count += 1
        return True

class Settings(BaseSettings):
    PROJECT_NAME: str = "Math Animator"
    API_V1_STR: str = "/api/v1"
    
    # OpenAI Configuration
    OPENAI_API_KEY: str
    
    # Database Configuration
    DATABASE_URL: str
    
    # Security
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # API Keys with rate limits
    API_KEYS: Dict[str, APIKey] = {
        "development": APIKey(
            key="dev_key_123",
            rate_limit=100,  # 100 requests per minute
            expires_at=None  # Never expires
        ),
        "production": APIKey(
            key="prod_key_456",
            rate_limit=60,   # 60 requests per minute
            expires_at=datetime.utcnow() + timedelta(days=365)
        )
    }
    
    # File Storage
    STORAGE_PATH: str
    MAX_UPLOAD_SIZE: int = 100 * 1024 * 1024  # 100MB
    
    # Redis Configuration
    REDIS_URL: str = "redis://localhost:6379/0"
    CACHE_TTL: int = 3600  # 1 hour
    
    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        case_sensitive = True

settings = Settings()