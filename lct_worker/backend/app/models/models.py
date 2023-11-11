from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr, validator, ConfigDict
from decimal import Decimal


class UserInDB(BaseModel):
    """
    User in database schema
    """
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    username: str
    hashed_password: str

class CamAction(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int | None = None
    cam_id: int
    time_detected: str
    comment: str
    detection: str
    precision: float
    frame: str

class VideoAction(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int | None = None
    video_id: int
    time_detected: str
    comment: str
    detection: str
    precision: float
    frame: str
