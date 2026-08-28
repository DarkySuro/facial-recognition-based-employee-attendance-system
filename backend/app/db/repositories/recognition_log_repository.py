from datetime import datetime

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