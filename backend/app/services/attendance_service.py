from dataclasses import dataclass
from datetime import date, datetime

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
    event: str


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

    def get_attendance(
        self,
        attendance_id: int,
    ):

        attendance = (
            self.attendance_repository.get_by_id(
                attendance_id
            )
        )

        if attendance is None:

            raise ValueError(
                f"Attendance record {attendance_id} "
                "not found."
            )

        return attendance


    def get_all_attendance(
        self,
    ):

        return (
            self.attendance_repository.get_all()
        )


    def get_employee_attendance(
        self,
        employee_id: int,
    ):

        return (
            self.attendance_repository
            .get_by_employee_id(
                employee_id
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
                event="already marked"
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
            event="marked"
        )

    def get_attendance_by_date_range(
        self,
        start_date: date,
        end_date: date,
    ):

        if start_date > end_date:
            raise ValueError(
                "Start date cannot be after end date."
            )

        return (
            self.attendance_repository
            .get_by_date_range(
                start_date=start_date,
                end_date=end_date,
            )
        )

    def get_employee_attendance_by_date_range(
        self,
        employee_id: int,
        start_date: date,
        end_date: date,
    ):

        if start_date > end_date:
            raise ValueError(
                "Start date cannot be after end date."
            )

        return (
            self.attendance_repository
            .get_by_employee_and_date_range(
                employee_id=employee_id,
                start_date=start_date,
                end_date=end_date,
            )
        )