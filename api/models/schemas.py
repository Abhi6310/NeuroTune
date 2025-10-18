from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime
from typing import Optional, Dict, Any, List
from enum import Enum

#Enums
class NeurotypeEnum(str, Enum):
    ADHD = "ADHD"
    AUTISM = "Autism"
    ANXIETY = "Anxiety"
    DEPRESSION = "Depression"
    NEUROTYPICAL = "Neurotypical"
    OTHER = "Other"

class AudioTypeEnum(str, Enum):
    BINAURAL = "binaural"
    ISOCHRONIC = "isochronic"
    WHITE_NOISE = "white_noise"
    NATURE = "nature"
    AMBIENT = "ambient"

#Response Schema
class APIResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None

#Error Schema
class ErrorResponse(BaseModel):
    success: bool = False
    error: str
    details: Optional[str] = None

#User Schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    neurotype: Optional[NeurotypeEnum] = None
    volume_preference: float = Field(0.5, ge=0.0, le=1.0)

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserResponse(UserBase):
    id: int
    created_at: datetime
    last_active: datetime
    activity: bool
    class Config:
        from_attributes = True

#updating user preferences
class UserPreferencesUpdate(BaseModel):
    neurotype: Optional[NeurotypeEnum] = None
    volume_preference: Optional[float] = Field(None, ge=0.0, le=1.0)
    sensory_preferences: Optional[List[str]] = None

#Audio Track Schemas
class AudioTrackBase(BaseModel):
    name: str = Field(..., max_length=100)
    audio_type: AudioTypeEnum
    duration: float = Field(..., ge=1)
    frequency: Optional[float] = Field(None, ge=0, le=1000)
    bpm: Optional[float] = Field(None, ge=20, le=200)

class AudioTrackResponse(AudioTrackBase):
    id: int
    file_path: str
    tags: Optional[List[str]] = None
    created_at: datetime
    activity: bool
    class Config:
        from_attributes = True



    



