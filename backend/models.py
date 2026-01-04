from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import datetime
import uuid

class ContactSubmissionCreate(BaseModel):
    """Model for creating a new contact submission"""
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    subject: str = Field(..., min_length=3, max_length=200)
    message: str = Field(..., min_length=10, max_length=2000)
    
    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Name cannot be empty')
        return v.strip()
    
    @validator('subject')
    def subject_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Subject cannot be empty')
        return v.strip()
    
    @validator('message')
    def message_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Message cannot be empty')
        return v.strip()

class ContactSubmission(BaseModel):
    """Complete contact submission model with metadata"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    email: str
    subject: str
    message: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    status: str = Field(default="new")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class ContactSubmissionResponse(BaseModel):
    """Response model for contact submission"""
    success: bool
    message: str
    id: Optional[str] = None

class ErrorResponse(BaseModel):
    """Error response model"""
    success: bool = False
    error: str
