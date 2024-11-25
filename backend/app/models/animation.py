from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class AnimationRequest(BaseModel):
    description: str = Field(..., min_length=10, max_length=1000)
    quality: str = Field(default="medium", pattern="^(low|medium|high)$")
    customization: Optional[dict] = None

class AnimationResponse(BaseModel):
    status: str
    animation_url: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    processing_time: Optional[float] = None
    quality: str

class AnimationHistoryResponse(BaseModel):
    id: int
    description: str
    url: str
    created_at: datetime
    quality: str

class AnimationError(BaseModel):
    status: str = "error"
    detail: str
    error_code: str 