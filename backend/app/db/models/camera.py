from datetime import datetime

from sqlalchemy import Boolean, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.db.database import Base

class Camera(Base):
  __tablename__ = "cameras"

  id: Mapped[int] = mapped_column(
    primary_key=True,
    autoincrement=True,
  )

  camera_code: Mapped[str] = mapped_column(
    String(50),
    unique=True,
    index=True,
    nullable=False,
  )

  name: Mapped[str] = mapped_column(
    String(100),
    nullable=False,
  )

  location: Mapped[str | None] = mapped_column(
    String(255),
    nullable=True,
  )

  source: Mapped[str] = mapped_column(
    String(255),
    nullable=False,
  )

  is_active: Mapped[bool] = mapped_column(
    Boolean,
    default=True,
    nullable=False,
  )

  created_at: Mapped[datetime] = mapped_column(
    DateTime,
    server_default=func.now(),
    nullable=False,
  )

  recognition_logs =relationship(
    "RecognitionLog",
    back_populates="camera",
  )