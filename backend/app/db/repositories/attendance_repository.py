from datetime import date, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.db.models.attendance import (
    Attendance,
)


class AttendanceRepository:

    def __init__(
        self,
        session: Session,
    ):
        self.session = session

    # ------------------------------------------
    # Get attendance by employee and date
    # ------------------------------------------

    def get_by_employee_and_date(
        self,
        employee_id: int,
        attendance_date: date,
    ) -> Attendance | None:

        statement = (
            select(Attendance)
            .where(
                Attendance.employee_id
                == employee_id,
                Attendance.attendance_date
                == attendance_date,
            )
        )

        return self.session.scalar(
            statement
        )

    # ------------------------------------------
    # Get attendance by ID
    # ------------------------------------------

    def get_by_id(
        self,
        attendance_id: int,
    ) -> Attendance | None:

        statement = select(
            Attendance
        ).where(
            Attendance.id == attendance_id
        )

        return self.session.scalar(
            statement
        )

    # ------------------------------------------
    # Get attendance by employee
    # ------------------------------------------

    def get_by_employee_id(
        self,
        employee_id: int,
    ) -> list[Attendance]:

        statement = (
            select(Attendance)
            .where(
                Attendance.employee_id
                == employee_id
            )
            .order_by(
                Attendance.attendance_date.desc()
            )
        )

        return list(
            self.session.scalars(
                statement
            )
        )

    # ------------------------------------------
    # Get all attendance records
    # ------------------------------------------

    def get_all(
        self,
    ) -> list[Attendance]:

        statement = (
            select(Attendance)
            .order_by(
                Attendance.attendance_date.desc(),
                Attendance.check_in_time.desc(),
            )
        )

        return list(
            self.session.scalars(
                statement
            )
        )
    # ----------------------------------------
    # Create check-in
    # ----------------------------------------

    def create_check_in(
        self,
        employee_id: int,
        check_in_time: datetime,
        recognition_confidence: float,
        status: str = "present",
    ) -> Attendance:

        attendance = Attendance(
            employee_id=employee_id,
            attendance_date=check_in_time.date(),
            check_in_time=check_in_time,
            status=status,
            recognition_confidence=(
                recognition_confidence
            ),
        )

        self.session.add(attendance)

        return attendance