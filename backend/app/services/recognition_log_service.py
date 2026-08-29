from datetime import date, datetime

from sqlalchemy.orm import Session

from backend.app.db.repositories.recognition_log_repository import (
    RecognitionLogRepository,
)


class RecognitionLogService:

    def __init__(
        self,
        session: Session,
    ):

        self.session = session

        self.repository = (
            RecognitionLogRepository(
                session
            )
        )

    def get_log(
        self,
        log_id: int,
    ):

        recognition_log = (
            self.repository.get_by_id(
                log_id
            )
        )

        if recognition_log is None:

            raise ValueError(
                f"Recognition log {log_id} "
                "not found."
            )

        return recognition_log


    def get_all_logs(
        self,
    ):

        return self.repository.get_all()


    def get_employee_logs(
        self,
        employee_id: int,
    ):

        return self.repository.get_by_employee_id(
            employee_id
        )


    def get_camera_logs(
        self,
        camera_id: int,
    ):

        return self.repository.get_by_camera_id(
            camera_id
        )

    def log(
        self,
        employee_id: int | None,
        recognized: bool,
        confidence: float | None,
        processing_time_ms: int | None,
        camera_id: int | None = None,
        timestamp: datetime | None = None,
    ) -> None:

        if timestamp is None:
            timestamp = datetime.now()

        try:
            self.repository.create(
                employee_id=employee_id,
                camera_id=camera_id,
                recognized=recognized,
                confidence=confidence,
                processing_time_ms=processing_time_ms,
                timestamp=timestamp,
            )
            self.session.commit()
            
        except Exception:
            self.session.rollback()
            raise

    def get_filtered_logs(
        self,
        employee_id: int | None = None,
        camera_id: int | None = None,
        recognized: bool | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ):

        if (
            start_date is not None
            and end_date is not None
            and start_date > end_date
        ):

            raise ValueError(
                "Start date cannot be after end date."
            )

        return self.repository.get_filtered(
            employee_id=employee_id,
            camera_id=camera_id,
            recognized=recognized,
            start_date=start_date,
            end_date=end_date,
        )