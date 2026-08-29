from datetime import date
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session

from backend.app.db.database import get_db

from backend.app.schemas.attendance import (
    AttendanceResponse,
)

from backend.app.services.attendance_service import (
    AttendanceService,
)


router = APIRouter(
    prefix="/attendance",
    tags=["Attendance"],
)


# ------------------------------------------
# Get all attendance records
# ------------------------------------------

@router.get(
    "",
    response_model=list[AttendanceResponse],
)
def get_all_attendance(
    start_date: date | None = None,
    end_date: date | None = None,
    db: Session = Depends(get_db),
):

    service = AttendanceService(
        db
    )

    if (
        start_date is None
        and end_date is None
    ):
        return service.get_all_attendance()

    if (
        start_date is None
        or end_date is None
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Both start_date and end_date "
                "must be provided together."
            )
        )
    try:
        return (
            service.get_attendance_by_date_range(
                start_date=start_date,
                end_date=end_date,
            )
        )
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )


# ------------------------------------------
# Get attendance by employee
#
# IMPORTANT:
# Must appear before /{attendance_id}
# ------------------------------------------

@router.get(
    "/employee/{employee_id}",
    response_model=list[AttendanceResponse],
)
def get_employee_attendance(
    employee_id: int,
    start_date: date | None,
    end_date: date | None,
    db: Session = Depends(get_db),
):

    service = AttendanceService(
        db
    )

    if (
        start_date is None
        and end_date is None
    ):
        return service.get_employee_attendance(
            employee_id
        )
    
    if (
        start_date is None
        or end_date is None
    ):

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Both start_date and end_date "
                "must be provided together."
            ),
        )

    try:

        return (
            service
            .get_employee_attendance_by_date_range(
                employee_id=employee_id,
                start_date=start_date,
                end_date=end_date,
            )
        )

    except ValueError as error:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        )

# ------------------------------------------
# Get attendance by ID
# ------------------------------------------

@router.get(
    "/{attendance_id}",
    response_model=AttendanceResponse,
)
def get_attendance(
    attendance_id: int,
    db: Session = Depends(get_db),
):

    service = AttendanceService(
        db
    )

    try:

        return service.get_attendance(
            attendance_id
        )

    except ValueError as error:

        raise HTTPException(
            status_code=(
                status.HTTP_404_NOT_FOUND
            ),
            detail=str(error),
        )