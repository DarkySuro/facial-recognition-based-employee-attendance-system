from datetime import date, datetime

from sqlalchemy import (
  Date,
  DateTime,
  Float,
  ForeignKey,
  String,
  UniqueConstraint,
  func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.db.database import Base

class Attendance(Base):
  __tablename__ = "attendance"

  __table_args__ = (
    UniqueConstraint(
      "employee_id",
      "attendance_date",
      name="uq_employee_attendance_date",
    ),
  )

  id: Mapped[int] = mapped_column(
    primary_key=True,
    autoincrement=True,
  )

  employee_id: Mapped[int] = mapped_column(
    ForeignKey("employees.id"),
    nullable=False,
    index=True,
  )

  attendance_date: Mapped[date] = mapped_column(
    Date,
    nullable=False,
  )

  check_in_time: Mapped[datetime] = mapped_column(
    DateTime,
    nullable=False,
  )

  check_out_time: Mapped[datetime | None] = mapped_column(
      DateTime,
      nullable=True,
  )

  status: Mapped[str] = mapped_column(
    String(50),
    default="present",
    nullable=False,
  )

  recognition_confidence: Mapped[float | None] = mapped_column(
      Float,
      nullable=True
  )

  created_at: Mapped[datetime] = mapped_column(
    DateTime,
    server_default=func.now(),
    nullable=False,
  )

  updated_at: Mapped[datetime] = mapped_column(
    DateTime,
    server_default=func.now(),
    onupdate=func.now(),
    nullable=False,
  )

  employee = relationship(
    "Employee",
    back_populates="attendance_records",
  )

