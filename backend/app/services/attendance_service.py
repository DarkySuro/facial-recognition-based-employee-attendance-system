from dataclasses import dataclass
from datetime import datetime

from sqlalchemy.orm import Session

from backend.app.db.repositories.attendance_repository import (
    AttendanceRepository,
)


@dataclass
class AttendanceResult:
    employee_id: int
    attendance_marked: bool
    already_marked: bool
    attendance_id: int | None
    check_in_time: datetime | None


class AttendanceService:

    def __init__(
        self,
        session: Session,
    ):
        self.session = session

        self.attendance_repository = (
            AttendanceRepository(
                session
            )
        )

    def mark_attendance(
        self,
        employee_id: int,
        recognition_confidence: float,
        timestamp: datetime | None = None,
    ) -> AttendanceResult:

        if timestamp is None:
            timestamp = datetime.now()

        attendance_date = timestamp.date()

        # ----------------------------------------
        # Check existing attendance
        # ----------------------------------------

        existing_attendance = (
            self.attendance_repository
            .get_by_employee_and_date(
                employee_id=employee_id,
                attendance_date=attendance_date,
            )
        )

        if existing_attendance is not None:

            return AttendanceResult(
                employee_id=employee_id,
                attendance_marked=False,
                already_marked=True,
                attendance_id=existing_attendance.id,
                check_in_time=(
                    existing_attendance.check_in_time
                ),
            )

        # ----------------------------------------
        # Create attendance
        # ----------------------------------------

        try:

            attendance = (
                self.attendance_repository
                .create_check_in(
                    employee_id=employee_id,
                    check_in_time=timestamp,
                    recognition_confidence=(
                        recognition_confidence
                    ),
                )
            )

            self.session.commit()

            self.session.refresh(
                attendance
            )

        except Exception:

            self.session.rollback()

            raise

        return AttendanceResult(
            employee_id=employee_id,
            attendance_marked=True,
            already_marked=False,
            attendance_id=attendance.id,
            check_in_time=(
                attendance.check_in_time
            ),
        )