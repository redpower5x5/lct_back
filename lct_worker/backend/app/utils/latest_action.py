from app.config import settings

from app.core import crud
from app.schemas import response_schemas
from sqlalchemy.orm import Session

latest_action_cache = {}

def latest_action(db: Session, user_id: int, video_id: int):
    """Get latest action for video.

    Args:
        db (Session): Database session.
        user_id (int): User id.
        video_id (int): Video id.
    """
    global latest_action_cache
    latest_action = crud.get_latest_action(db=db, user_id=user_id, video_id=video_id)
    # check if keys exist
    if user_id not in latest_action_cache:
        latest_action_cache[user_id] = {}
    if video_id not in latest_action_cache[user_id]:
        latest_action_cache[user_id][video_id] = None
    if latest_action_cache[user_id][video_id] is None:
        latest_action_cache[user_id][video_id] = latest_action.id
        return latest_action
    if latest_action.id <= latest_action_cache[user_id][video_id]:
        return None

    return latest_action

def purge_latest_action_cache(user_id: int, video_id: int):
    """Purge latest action cache."""

    global latest_action_cache
    latest_action_cache[user_id][video_id] = None