from datetime import datetime

from pydantic import BaseModel, ConfigDict


class RecognitionLogResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int

    employee_id: int | None

    camera_id: int | None

    recognized: bool

    confidence: float | None

    processing_time_ms: int | None

    timestamp: datetime