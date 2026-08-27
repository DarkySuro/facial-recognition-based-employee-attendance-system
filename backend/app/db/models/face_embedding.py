from datetime import datetime

from sqlalchemy import (
  Boolean,
  DateTime,
  ForeignKey,
  Integer,
  LargeBinary,
  String,
  func
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.db.database import Base

class FaceEmbedding(Base): 
  __tablename__ = "face_embeddings"

  id: Mapped[int] = mapped_column(
    primary_key=True,
    autoincrement=True,
  )

  employee_id: Mapped[int] = mapped_column(
    ForeignKey("employees.id", ondelete="CASCADE"),
    nullable=False,
    index=True,
  )

  embedding: Mapped[bytes] = mapped_column(
    LargeBinary,
    nullable=False,
  )

  model_name: Mapped[str] = mapped_column(
    String(100),
    nullable=False,
  )

  embedding_dimension: Mapped[int] = mapped_column(
    Integer,
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

  employee = relationship(
    "Employee",
    back_populates="face_embeddings",
  )