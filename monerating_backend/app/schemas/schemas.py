from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    name: str
    email: EmailStr
    timezone: str = "UTC"


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class MoodLogBase(BaseModel):
    user_id: int
    timestamp: Optional[datetime] = None
    mood_score: int = Field(ge=1, le=10)
    mood_tags: str = ""
    note_text: str = ""
    sentiment_score: Optional[float] = None


class MoodLogCreate(MoodLogBase):
    pass


class MoodLogRead(MoodLogBase):
    id: int

    class Config:
        orm_mode = True


class JournalEntryBase(BaseModel):
    user_id: int
    timestamp: Optional[datetime] = None
    text: str = ""
    sentiment_score: Optional[float] = None
    keywords: str = ""


class JournalEntryCreate(JournalEntryBase):
    pass


class JournalEntryRead(JournalEntryBase):
    id: int

    class Config:
        orm_mode = True


class WearableReadingBase(BaseModel):
    user_id: int
    timestamp: Optional[datetime] = None
    type: str
    value: float
    device: str = "unknown"


class WearableReadingCreate(WearableReadingBase):
    pass


class WearableReadingRead(WearableReadingBase):
    id: int

    class Config:
        orm_mode = True


class AlertBase(BaseModel):
    user_id: int
    timestamp: Optional[datetime] = None
    type: str
    message: str
    resolved: bool = False


class AlertCreate(AlertBase):
    pass


class AlertRead(AlertBase):
    id: int

    class Config:
        orm_mode = True

