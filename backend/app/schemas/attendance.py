from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


class AttendanceResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int

    employee_id: int

    attendance_date: date

    check_in_time: datetime

    check_out_time: datetime | None

    status: str

    recognition_confidence: float | None

    created_at: datetime

    updated_at: datetime