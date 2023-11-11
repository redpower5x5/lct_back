from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks

from sqlalchemy.orm import Session

from app.config import log
from app.schemas import response_schemas, request_schemas
from app.core.dependencies import get_db
from app.core import crud
from app.config import settings
from app.utils.token import get_current_active_user
from app.ai.process_data import run_on_file
from fastapi import File, UploadFile
import os

router = APIRouter(
    prefix="/files",
    tags=["files"],
)


@router.post("/addfile", response_model=response_schemas.Video)
async def add_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    current_user: response_schemas.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Add a file
    """
    result = None
    try:
        file_name = f'{current_user.id}_{file.filename}'
        path_to_file = f'{settings.UPLOAD_FOLDER}/{file_name}'
        with open(path_to_file, 'wb') as f:
            while contents := file.file.read(1024 * 1024):
                f.write(contents)
        result = crud.add_video(db=db, video_file_path=file_name, user_id=current_user.id)
        log.debug(f"File {file_name} uploaded")
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File not uploaded",
        )
    finally:
        file.file.close()
    background_tasks.add_task(run_on_file, path_to_file, db, result.id)
    log.debug(f"File {file_name} processing started")

    return result


@router.delete("/deletefile/{file_id}", response_model=response_schemas.Video)
async def delete_file(
    file_id: int,
    current_user: response_schemas.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Delete a file
    """
    res = crud.delete_video(db=db, video_id=file_id, user_id=current_user.id)
    if res:
        # delet file from storage
        path_to_file = f'{settings.UPLOAD_FOLDER}/{res.video_file_path}'
        os.remove(path_to_file)
    return res

@router.get("/allfiles", response_model=response_schemas.AllVideos)
async def get_all_files(
    current_user: response_schemas.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Get all files
    """
    return crud.get_all_videos(db=db, user_id=current_user.id)

@router.get("/getfile/{file_id}/actions", response_model=response_schemas.VideoActionsList)
async def get_file_actions(
    file_id: int,
    current_user: response_schemas.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Get all actions for file
    """
    return crud.get_user_video_actions(db=db, video_id=file_id, user_id=current_user.id)
