from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import CursorResult

from sqlalchemy.orm import Session

from app.config import log
from app.schemas import response_schemas, request_schemas
from app.core.dependencies import get_db
from app.core import crud
from app.config import settings
from app.utils.token import get_current_active_user

from fastapi_cache.decorator import cache

import time

router = APIRouter(
    prefix="/cams",
    tags=["cams"],
)


@router.get("/all", response_model=response_schemas.AllCams)
@cache(expire=settings.CACHE_EXPIRE)
async def get_cams(
    current_user: response_schemas.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Get all cams
    """
    cams = crud.get_all_cams(db=db)

    if cams is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No cams found",
        )

    return cams


@router.post("/create", response_model=None)
async def create_cam(
    cam: request_schemas.CamCreate,
    current_user: response_schemas.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Create a post
    """
    return crud.create_cam(db=db, cam=cam)


@router.get("/get/{cam_id}", response_model=response_schemas.Cam)
async def get_cam(
    cam_id: int,
    current_user: response_schemas.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Get a post
    """
    cam = crud.get_cam(db=db, cam_id=cam_id)

    if cam is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No cam found",
        )

    return cam

@router.delete("/delete/{cam_id}", response_model=response_schemas.Cam)
async def delete_post(
    cam_id: int,
    current_user: response_schemas.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Delete a post
    """
    deleting_op = crud.delete_cam(
        db=db,
        cam_id=cam_id
    )

    if deleting_op is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No cam found",
        )


@router.put("/update", response_model=response_schemas.Cam)
async def update_cam(
    cam: request_schemas.CamUpdate,
    current_user: response_schemas.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Update a post
    """
    return crud.update_cam(db=db, cam=cam)

@router.get("/get/{cam_id}/actions", response_model=response_schemas.CamActionsList)
async def get_cam_actions(
    cam_id: int,
    current_user: response_schemas.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Get a post
    """
    cam_actions = crud.get_cam_actions(db=db, cam_id=cam_id)

    if cam_actions is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No cam found",
        )

    return cam_actions
