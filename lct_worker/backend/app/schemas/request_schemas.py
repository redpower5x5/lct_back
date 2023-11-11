from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr, validator
from decimal import Decimal


class UserCreate(BaseModel):
    """
    User create schema
    """

    email: EmailStr
    password: str
    username: str


class UserLogin(BaseModel):
    """
    User login schema
    """

    email: EmailStr
    password: str


class CamUpdate(BaseModel):
    """
    Cam update schema
    """

    id: int
    address: str
    longitude: Decimal
    latitude: Decimal
    rtsp_link: str

    model_config = {
        "json_schema_extra": {
            "example": {"id": 1, "address": "address", "longitude": 0, "latitude": 0, "rtsp_link": "rtsp://"}
        }
    }


class CamCreate(BaseModel):
    """
    Cam create schema
    """

    address: str
    longitude: Decimal
    latitude: Decimal
    rtsp_link: str

    model_config = {
        "json_schema_extra": {
            "example": {"address": "address", "longitude": 0, "latitude": 0, "rtsp_link": "rtsp://"}
        }
    }


class ReactionCreate(BaseModel):
    """
    Reaction create schema
    """

    post_id: int
    reaction_type: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"post_id": 1, "reaction_type": "like"},
                {"post_id": 1, "reaction_type": "dislike"},
            ]
        }
    }


class ReactionDelete(BaseModel):
    post_id: int
