from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    status,
)
from sqlalchemy.orm import Session

from backend.app.db.database import get_db
from backend.app.schemas.camera import (
    CameraCreate,
    CameraResponse,
    CameraUpdate,
)
from backend.app.services.camera_service import (
    CameraService,
)


router = APIRouter(
    prefix="/cameras",
    tags=["Cameras"],
)


# ------------------------------------------
# Create camera
# ------------------------------------------

@router.post(
    "",
    response_model=CameraResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_camera(
    payload: CameraCreate,
    db: Session = Depends(get_db),
):

    service = CameraService(
        db
    )

    try:

        return service.create_camera(
            camera_code=payload.camera_code,
            name=payload.name,
            source=payload.source,
            location=payload.location,
        )

    except ValueError as error:

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        )


# ------------------------------------------
# Get all cameras
# ------------------------------------------

@router.get(
    "",
    response_model=list[CameraResponse],
)
def get_cameras(
    active_only: bool = Query(
        default=False,
    ),
    db: Session = Depends(get_db),
):

    service = CameraService(
        db
    )

    return service.get_cameras(
        active_only=active_only
    )


# ------------------------------------------
# Get camera by ID
# ------------------------------------------

@router.get(
    "/{camera_id}",
    response_model=CameraResponse,
)
def get_camera(
    camera_id: int,
    db: Session = Depends(get_db),
):

    service = CameraService(
        db
    )

    try:

        return service.get_camera(
            camera_id
        )

    except ValueError as error:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        )


# ------------------------------------------
# Update camera
# ------------------------------------------

@router.patch(
    "/{camera_id}",
    response_model=CameraResponse,
)
def update_camera(
    camera_id: int,
    payload: CameraUpdate,
    db: Session = Depends(get_db),
):

    service = CameraService(
        db
    )

    try:

        return service.update_camera(
            camera_id=camera_id,
            name=payload.name,
            source=payload.source,
            location=payload.location,
            is_active=payload.is_active,
        )

    except ValueError as error:

        message = str(error)

        if "not found" in message.lower():

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=message,
            )

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=message,
        )