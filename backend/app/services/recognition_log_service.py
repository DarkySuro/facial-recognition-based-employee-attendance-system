from datetime import datetime

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