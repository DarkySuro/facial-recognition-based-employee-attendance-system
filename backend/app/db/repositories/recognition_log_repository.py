from datetime import date, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.db.models.recognition_log import (
    RecognitionLog,
)


class RecognitionLogRepository:

    def __init__(
        self,
        session: Session,
    ):
        self.session = session

    # ------------------------------------------
    # Create recognition log
    # ------------------------------------------

    def create(
        self,
        employee_id: int | None,
        camera_id: int | None,
        recognized: bool,
        confidence: float | None,
        processing_time_ms: int | None,
        timestamp: datetime,
    ) -> RecognitionLog:

        recognition_log = RecognitionLog(
            employee_id=employee_id,
            camera_id=camera_id,
            recognized=recognized,
            confidence=confidence,
            processing_time_ms=processing_time_ms,
            timestamp=timestamp,
        )

        self.session.add(
            recognition_log
        )

        return recognition_log

    # ------------------------------------------
    # Get log by ID
    # ------------------------------------------
    def get_by_id(
        self,
        log_id: int,
    ) -> RecognitionLog | None:

        statement = select(
            RecognitionLog
        ).where(
            RecognitionLog.id == log_id
        )

        return self.session.scalar(
            statement
        )

    # ------------------------------------------
    # Get all logs
    # ------------------------------------------
    def get_all(
        self,
    ) -> list[RecognitionLog]:

        statement = (
            select(RecognitionLog)
            .order_by(
                RecognitionLog.timestamp.desc()
            )
        )

        return list(
            self.session.scalars(
                statement
            )
        )

    # ------------------------------------------
    # Get logs by employee
    # ------------------------------------------
    def get_by_employee_id(
        self,
        employee_id: int,
    ) -> list[RecognitionLog]:

        statement = (
            select(RecognitionLog)
            .where(
                RecognitionLog.employee_id
                == employee_id
            )
            .order_by(
                RecognitionLog.timestamp.desc()
            )
        )

        return list(
            self.session.scalars(
                statement
            )
        )

    # ------------------------------------------
    # Get logs by camera
    # ------------------------------------------
    def get_by_camera_id(
        self,
        camera_id: int,
    ) -> list[RecognitionLog]:

        statement = (
            select(RecognitionLog)
            .where(
                RecognitionLog.camera_id
                == camera_id
            )
            .order_by(
                RecognitionLog.timestamp.desc()
            )
        )

        return list(
            self.session.scalars(
                statement
            )
        )

    def get_filtered(
        self,
        employee_id: int | None = None,
        camera_id: int | None = None,
        recognized: bool | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> list[RecognitionLog]:

        statement = select(
            RecognitionLog
        )

        if employee_id is not None:

            statement = statement.where(
                RecognitionLog.employee_id
                == employee_id
            )

        if camera_id is not None:

            statement = statement.where(
                RecognitionLog.camera_id
                == camera_id
            )

        if recognized is not None:

            statement = statement.where(
                RecognitionLog.recognized
                == recognized
            )

        if start_date is not None:

            statement = statement.where(
                RecognitionLog.timestamp
                >= datetime.combine(
                    start_date,
                    datetime.min.time(),
                )
            )

        if end_date is not None:

            statement = statement.where(
                RecognitionLog.timestamp
                < datetime.combine(
                    end_date,
                    datetime.max.time(),
                )
            )

        statement = statement.order_by(
            RecognitionLog.timestamp.desc()
        )

        return list(
            self.session.scalars(
                statement
            )
        )