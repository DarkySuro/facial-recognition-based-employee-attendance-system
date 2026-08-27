from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Integer,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.db.database import Base


class RecognitionLog(Base):
    __tablename__ = "recognition_logs"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    employee_id: Mapped[int | None] = mapped_column(
        ForeignKey("employees.id"),
        nullable=True,
        index=True,
    )

    camera_id: Mapped[int | None] = mapped_column(
        ForeignKey("cameras.id"),
        nullable=True,
        index=True,
    )

    recognized: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )

    confidence: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    processing_time_ms: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    timestamp: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )

    employee = relationship(
        "Employee",
        back_populates="recognition_logs",
    )

    camera = relationship(
        "Camera",
        back_populates="recognition_logs",
    )