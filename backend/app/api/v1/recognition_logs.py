from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session

from backend.app.db.database import get_db

from backend.app.schemas.recognition_log import (
    RecognitionLogResponse,
)

from backend.app.services.recognition_log_service import (
    RecognitionLogService,
)


router = APIRouter(
    prefix="/recognition-logs",
    tags=["Recognition Logs"],
)


# ------------------------------------------
# Get all recognition logs
# ------------------------------------------

@router.get(
    "",
    response_model=list[RecognitionLogResponse],
)
def get_all_logs(
    db: Session = Depends(get_db),
):

    service = RecognitionLogService(
        db
    )

    return service.get_all_logs()


# ------------------------------------------
# Get logs by employee
#
# Must appear before /{log_id}
# ------------------------------------------

@router.get(
    "/employee/{employee_id}",
    response_model=list[RecognitionLogResponse],
)
def get_employee_logs(
    employee_id: int,
    db: Session = Depends(get_db),
):

    service = RecognitionLogService(
        db
    )

    return service.get_employee_logs(
        employee_id
    )


# ------------------------------------------
# Get logs by camera
#
# Must appear before /{log_id}
# ------------------------------------------

@router.get(
    "/camera/{camera_id}",
    response_model=list[RecognitionLogResponse],
)
def get_camera_logs(
    camera_id: int,
    db: Session = Depends(get_db),
):

    service = RecognitionLogService(
        db
    )

    return service.get_camera_logs(
        camera_id
    )


# ------------------------------------------
# Get log by ID
# ------------------------------------------

@router.get(
    "/{log_id}",
    response_model=RecognitionLogResponse,
)
def get_log(
    log_id: int,
    db: Session = Depends(get_db),
):

    service = RecognitionLogService(
        db
    )

    try:

        return service.get_log(
            log_id
        )

    except ValueError as error:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        )