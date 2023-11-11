from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Enum,
    UniqueConstraint,
    TEXT,
    Numeric
)
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

Base = declarative_base()


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(20), nullable=False)
    email = Column(String(50), nullable=False)
    hashed_password = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.now())

class Cams(Base):
    __tablename__ = "cams"
    id = Column(Integer, primary_key=True)
    rtsp_link = Column(TEXT, nullable=False)
    address = Column(String(500), nullable=False)
    longitude = Column(Numeric(11, 8), nullable=False)
    latitude = Column(Numeric(11, 8), nullable=False)
    created_at = Column(DateTime, default=datetime.now())

class CamDetections(Base):
    __tablename__ = "cam_detections"
    id = Column(Integer, primary_key=True)
    detection = Column(String(100), nullable=False)
    precision = Column(Numeric(5, 2), nullable=False)
    time_detected = Column(TEXT, nullable=False)
    comment = Column(TEXT, nullable=True)
    frame = Column(TEXT, nullable=False)
    cam_id = Column(Integer, ForeignKey("cams.id"))
    created_at = Column(DateTime, default=datetime.now())

class Videos(Base):
    __tablename__ = "videos"
    id = Column(Integer, primary_key=True)
    video_file_path = Column(TEXT, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.now())

class VideoDetections(Base):
    __tablename__ = "video_detections"
    id = Column(Integer, primary_key=True)
    detection = Column(String(100), nullable=False)
    precision = Column(Numeric(5, 2), nullable=False)
    time_detected = Column(TEXT, nullable=False)
    comment = Column(TEXT, nullable=True)
    frame = Column(TEXT, nullable=False)
    video_id = Column(Integer, ForeignKey("videos.id"))
    created_at = Column(DateTime, default=datetime.now())
