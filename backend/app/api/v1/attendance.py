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
    db: Session = Depends(get_db),
):

    service = AttendanceService(
        db
    )

    return service.get_all_attendance()


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
    db: Session = Depends(get_db),
):

    service = AttendanceService(
        db
    )

    return service.get_employee_attendance(
        employee_id
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