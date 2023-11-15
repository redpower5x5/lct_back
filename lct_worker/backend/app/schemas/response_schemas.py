from typing import Optional, List, Dict, Union
from pydantic import BaseModel, Field, EmailStr, validator, ConfigDict
from decimal import Decimal


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: str
    disabled: bool | None = None


class Cam(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int | None = None
    address: str
    longitude: float
    latitude: float
    rtsp_link: str

class Video(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int | None = None
    video_file_path: str
    user_id: int


class CamAction(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int | None = None
    cam_id: int
    time_detected: str
    comment: str
    detection: str
    precision: Decimal
    frame: str

class CamActionsList(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    actions: List[CamAction]


class VideoAction(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int | None = None
    video_id: int
    detection: str
    precision: Decimal
    time_detected: str
    comment: str

class VideoActionFrame(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int | None = None
    video_id: int
    frame: str

class VideoActionsList(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    actions: List[VideoAction]


class AllCams(BaseModel):
    count: int
    cams: List[Cam]

class AllVideos(BaseModel):
    count: int
    videos: List[Video]
