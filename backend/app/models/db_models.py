from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean
from sqlalchemy.sql import func
from app.core.database import Base

class Animation(Base):
    __tablename__ = "animations"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(Text, nullable=False)
    manim_code = Column(Text, nullable=False)
    animation_url = Column(String, nullable=True)
    quality = Column(String, nullable=False, default="medium")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now()) 