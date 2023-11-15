from sqlalchemy import update
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from typing import Union

from app.models import db_models, models
from app.schemas import response_schemas, request_schemas
from app.config import log
from app.utils.token import get_password_hash


def get_user(db: Session, email: Union[str, None]) -> Union[models.UserInDB, None]:
    try:
        return models.UserInDB.model_validate(
            db.query(
                db_models.Users.id.label("id"),
                db_models.Users.username.label("username"),
                db_models.Users.email.label("email"),
                db_models.Users.hashed_password.label("hashed_password"),
            )
            .filter(
                db_models.Users.email == email,
            )
            .one()
        )
    except NoResultFound:
        return None


def get_post_author_id(db: Session, post_id: int) -> Union[int, None]:
    try:
        return (
            db.query(db_models.Posts.user_id)
            .filter(db_models.Posts.id == post_id)
            .one()[0]
        )
    except NoResultFound:
        return None


def create_user(db: Session, user: request_schemas.UserCreate) -> response_schemas.User:
    db_user = db_models.Users(
        email=user.email,
        username=user.username,
        hashed_password=get_password_hash(user.password),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    db_user = response_schemas.User.model_validate(db_user)

    log.info(f"Created user: {db_user}")
    return db_user


def create_cam(
    db: Session, cam: request_schemas.CamCreate) -> response_schemas.Cam:
    db_cam = db_models.Cams(
        address=cam.address,
        longitude=cam.longitude,
        latitude=cam.latitude,
        rtsp_link=cam.rtsp_link
    )
    db.add(db_cam)
    db.commit()
    db.refresh(db_cam)

    db_cam = response_schemas.Cam.model_validate(db_cam)

    log.info(f"Created cam {db_cam}")
    return db_cam

def get_cam(
    db: Session, cam_id: int) -> Union[response_schemas.Cam, None]:
    try:
        return response_schemas.Cam.model_validate(
            db.query(
                db_models.Cams.id.label("id"),
                db_models.Cams.address.label("address"),
                db_models.Cams.longitude.label("longitude"),
                db_models.Cams.latitude.label("latitude"),
                db_models.Cams.rtsp_link.label("rtsp_link"),
            )
            .filter(
                db_models.Cams.id == cam_id,
            )
            .one()
        )
    except NoResultFound:
        return None

def delete_cam(
    db: Session, cam_id: int) -> Union[response_schemas.Cam, None]:
    try:
        db_cam = (
            db.query(db_models.Cams)
            .filter(
                db_models.Cams.id == cam_id)
            .one()
        )
        db.delete(db_cam)
        db.commit()

        db_cam = response_schemas.Cam.model_validate(db_cam)

        log.info(f"Deleted cam {db_cam}")
        return db_cam
    except NoResultFound:
        return None


def chech_is_cam_exists(db: Session, cam_id: int) -> bool:
    try:
        db.query(db_models.Cams).filter(db_models.Cams.id == cam_id).one()
        return True
    except NoResultFound:
        return False


def update_cam(
    db: Session, cam: request_schemas.CamUpdate) -> Union[response_schemas.Cam, None]:
    db_cam = db.query(db_models.Cams).filter(db_models.Cams.id == cam.id).first()

    if db_cam is None:
        return None

    db_cam.address = cam.address
    db_cam.longitude = cam.longitude
    db_cam.latitude = cam.latitude
    db_cam.rtsp_link = cam.rtsp_link
    db.commit()
    db.refresh(db_cam)

    db_cam = response_schemas.Cam.model_validate(db_cam)

    log.info(f"Edited cam {db_cam}")

    return db_cam

def get_cam_actions(db: Session, cam_id: int) -> Union[response_schemas.CamActionsList, None]:
    try:
        return response_schemas.CamActionsList(
            actions=[
                response_schemas.CamAction.model_validate(action)
                for action in db.query(
                    db_models.CamDetections.id.label("id"),
                    db_models.CamDetections.cam_id.label("cam_id"),
                    db_models.CamDetections.time_detected.label("time_detected"),
                    db_models.CamDetections.frame.label("frame"),
                    db_models.CamDetections.comment.label("comment"),
                    db_models.CamDetections.detection.label("detection"),
                    db_models.CamDetections.precision.label("precision"),
                ).filter(
                    db_models.CamDetections.cam_id == cam_id
                ).all()
            ],
        )
    except NoResultFound:
        return None

def add_cam_action(
    db: Session, action: models.CamAction) -> Union[response_schemas.CamAction, None]:
    try:
        db_action = db_models.CamDetections(
            cam_id=action.cam_id,
            time_detected=action.time_detected,
            comment=action.comment,
            detection=action.detection,
            precision=action.precision,
            frame=action.frame
        )
        db.add(db_action)
        db.commit()
        db.refresh(db_action)
    except NoResultFound:
        return None


def get_all_cams(db: Session) -> Union[response_schemas.AllCams, None]:
    try:
        return response_schemas.AllCams(
            count=db.query(db_models.Cams).count(),
            cams=[
                response_schemas.Cam.model_validate(cam)
                for cam in db.query(
                    db_models.Cams.id.label("id"),
                    db_models.Cams.address.label("address"),
                    db_models.Cams.longitude.label("longitude"),
                    db_models.Cams.latitude.label("latitude"),
                    db_models.Cams.rtsp_link.label("rtsp_link"),
                ).all()
            ],
        )
    except NoResultFound:
        return None

def add_video(db: Session, video_file_path: str, user_id: int) -> response_schemas.Video:
    db_video = db_models.Videos(
        video_file_path=video_file_path,
        user_id=user_id
    )
    db.add(db_video)
    db.commit()
    db.refresh(db_video)

    db_video = response_schemas.Video.model_validate(db_video)

    log.info(f"Created video {db_video}")
    return db_video

def delete_video(db: Session, video_id: int, user_id: int) -> Union[response_schemas.Video, None]:
    try:
        db_video = (
            db.query(db_models.Videos)
            .filter(
                db_models.Videos.id == video_id,
                db_models.Videos.user_id == user_id
            )
            .one()
        )
        db.delete(db_video)
        db.commit()

        db_video = response_schemas.Video.model_validate(db_video)

        log.info(f"Deleted video {db_video}")
        return db_video
    except NoResultFound:
        return None

def get_all_videos(db: Session, user_id: int) -> Union[response_schemas.AllVideos, None]:
    try:
        return response_schemas.AllVideos(
            count=db.query(db_models.Videos).filter(db_models.Videos.user_id == user_id).count(),
            videos=[
                response_schemas.Video.model_validate(video)
                for video in db.query(
                    db_models.Videos.id.label("id"),
                    db_models.Videos.video_file_path.label("video_file_path"),
                    db_models.Videos.user_id.label("user_id"),
                ).filter(db_models.Videos.user_id == user_id).all()
            ],
        )
    except NoResultFound:
        return None

def get_user_video_actions(db: Session, user_id: int, video_id: int) -> Union[response_schemas.VideoActionsList, None]:
    try:
        return response_schemas.VideoActionsList(
            actions=[
                response_schemas.VideoAction.model_validate(action)
                for action in db.query(
                    db_models.VideoDetections.id.label("id"),
                    db_models.VideoDetections.video_id.label("video_id"),
                    db_models.VideoDetections.time_detected.label("time_detected"),
                    db_models.VideoDetections.comment.label("comment"),
                    db_models.VideoDetections.detection.label("detection"),
                    db_models.VideoDetections.precision.label("precision"),
                ).filter(
                    db_models.VideoDetections.video_id == video_id
                ).all()
            ],
        )
    except NoResultFound:
        return None

def get_latest_action(db: Session, user_id: int, video_id: int) -> Union[response_schemas.VideoAction, None]:
    try:
        return response_schemas.VideoAction.model_validate(
            db.query(
                db_models.VideoDetections.id.label("id"),
                db_models.VideoDetections.video_id.label("video_id"),
                db_models.VideoDetections.time_detected.label("time_detected"),
                db_models.VideoDetections.comment.label("comment"),
                db_models.VideoDetections.detection.label("detection"),
                db_models.VideoDetections.precision.label("precision"),
            ).filter(
                db_models.VideoDetections.video_id == video_id
            ).order_by(
                db_models.VideoDetections.id.desc()
            ).first()
        )
    except NoResultFound:
        return None

def get_action_frame(db: Session, user_id: int, video_id: int, action_id: int) -> Union[response_schemas.VideoActionFrame, None]:
    try:
        return response_schemas.VideoActionFrame(
            id=action_id,
            video_id=video_id,
            frame=db.query(
                    db_models.VideoDetections.frame.label("frame"),
                ).filter(
                    db_models.VideoDetections.video_id == video_id,
                    db_models.VideoDetections.id == action_id
                ).one()[0],
        )
    except NoResultFound:
        return None

def add_video_action(
    db: Session, action: models.VideoAction) -> Union[response_schemas.VideoAction, None]:
    try:
        db_action = db_models.VideoDetections(
            video_id=action.video_id,
            time_detected=action.time_detected,
            comment=action.comment,
            detection=action.detection,
            precision=action.precision,
            frame=action.frame
        )
        db.add(db_action)
        db.commit()
        db.refresh(db_action)
    except NoResultFound:
        return None