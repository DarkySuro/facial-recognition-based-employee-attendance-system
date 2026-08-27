from datetime import datetime

from sqlalchemy import Boolean, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.db.database import Base

class Employee(Base):
  __tablename__ = 'employees'

  id: Mapped[int] = mapped_column(
    primary_key=True,
    autoincrement=True,
  )

  employee_code: Mapped[str] = mapped_column(
    String(50),
    unique=True,
    index=True,
    nullable=False,
  )

  name: Mapped[str] = mapped_column(
    String(150),
    nullable=False,
  )

  email: Mapped[str | None] = mapped_column(
    String(150),
    unique=True,
    nullable=True,
  )

  department: Mapped[str | None] = mapped_column(
    String(100),
    nullable=True
  )

  designation: Mapped[str | None] = mapped_column(
    String(100),
    nullable=True,
  )

  is_active: Mapped[bool] = mapped_column(
    Boolean,
    default=True,
    nullable=False,
  )

  created_at: Mapped[datetime] = mapped_column(
    DateTime,
    server_default=func.now(),
    onupdate=func.now(),
    nullable=False,
  )

  face_embeddings = relationship(
    "FaceEmbedding",
    back_populates="employee",
    cascade="all, delete-orphan",
  )

  attendance_records = relationship(
    "Attendance",
    back_populates="employee",
  )

  recognition_logs = relationship(
    "RecognitionLog",
    back_populates="employee",
  )
