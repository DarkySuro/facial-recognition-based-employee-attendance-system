from datetime import date
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
@router.get(
    "",
    response_model=list[RecognitionLogResponse],
)
def get_all_logs(
    employee_id: int | None = None,
    camera_id: int | None = None,
    recognized: bool | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
    db: Session = Depends(get_db),
):

    service = RecognitionLogService(
        db
    )

    try:

        if (
            employee_id is None
            and camera_id is None
            and recognized is None
            and start_date is None
            and end_date is None
        ):

            return service.get_all_logs()

        if (
            start_date is None
            and end_date is not None
        ):

            raise ValueError(
                "start_date is required "
                "when end_date is provided."
            )

        if (
            start_date is not None
            and end_date is None
        ):

            raise ValueError(
                "end_date is required "
                "when start_date is provided."
            )

        return service.get_filtered_logs(
            employee_id=employee_id,
            camera_id=camera_id,
            recognized=recognized,
            start_date=start_date,
            end_date=end_date,
        )

    except ValueError as error:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        )


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