from dataclasses import dataclass
import numpy as np
from sqlalchemy import delete
from sqlalchemy.orm import Session

from backend.app.ai.embedding import (
  EMBEDDING_DIMENSION,
  serialize_embedding
)

from backend.app.ai.duplicate_detector import (
  DuplicateDetector
)

from backend.app.ai.enrollment_validator import (
  EnrollmentValidator
)

from backend.app.db.models.face_embedding import FaceEmbedding

from backend.app.db.repositories.employee_repository import EmployeeRepository

from backend.app.db.repositories.face_embedding_repository import (
  FaceEmbeddingRepository
)

@dataclass
class FaceEnrollmentResult:
  employee_id: int
  embeddings_saved: int
  minimum_similarity: float
  maximum_similarity: float
  average_similarity: float

class FaceEnrollmentService:

  def __init__(
      self,
      session: Session,
      consistency_threshold: float = 0.65,
      duplicate_threshold: float = 0.70
  ):

    self.session = session

    self.employee_repository = (
      EmployeeRepository(
        session
      )
    )

    self.embedding_repository = (
      FaceEmbeddingRepository(
        session
      )
    )

    self.validator = (
      EnrollmentValidator(
        minimum_similarity_threshold=(
          consistency_threshold
        )
      )
    )

    self.duplicate_detector = (
      DuplicateDetector(
        threshold=(
          duplicate_threshold
        )
      )
    )

  def enroll(
      self,
      employee_id: int,
      embeddings: list[np.ndarray],
      model_name: str = "buffalo_l"
  ) -> FaceEnrollmentResult:

    # -------------------------------------------
    # 1. Verify employee exists
    # -------------------------------------------

    employee = (
      self.employee_repository.get_by_id(
        employee_id=employee_id
      )
    )

    if employee is None:
      raise ValueError(
        f"Employee {employee_id} "
        "does not exist."
      )

    if not employee.is_active:
      raise ValueError(
        f"Employee {employee_id} "
        "is inactive."
      )

    # -------------------------------------------
    # 2.  
    # -------------------------------------------

    if not embeddings:
      raise ValueError(
        "No face embeddings provided!"
      )

    for embedding in embeddings:
      embedding = np.asarray(
        embedding,
        dtype=np.float32
      )

      # if embedding.ndim != 1:
      #   raise ValueError(
      #       f"Embedding must be 1-dimensional. "
      #       f"Received shape: {embedding.shape}"
      #   )

      if embedding.shape != (
        EMBEDDING_DIMENSION,
      ):
        raise ValueError(
          f"Invalid embedding shape: "
          f"Expected {EMBEDDING_DIMENSION}, "
          f"{embedding.shape[0]}"
        )


      print(
        "DEBUG:",
        "shape =", embedding.shape,
        "dimension =", EMBEDDING_DIMENSION,
        "type =", type(EMBEDDING_DIMENSION),
      )

    # ------------------------------------------
    # 3. Validate enrollment consistency
    # ------------------------------------------

    validation = (
      self.validator.validate(
          embeddings
      )
    )

    if not validation.valid:
      raise ValueError(
        validation.reason 
        or "Enrollment validation failed!"
      )

    # ------------------------------------------
    # 4. Check duplicate against OTHER employees
    # ------------------------------------------

    existing_embeddings = (
      self.embedding_repository.get_all_active(
        exclude_employee_id=employee_id
      )
    )

    duplicate = (
      self.duplicate_detector.check(
        new_embeddings=embeddings,
        existing_embeddings=existing_embeddings
      )
    )

    if duplicate.is_duplicate:

      raise ValueError(
          "Face already appears to be "
          f"registered to employee "
          f"{duplicate.matched_employee_id}. "
          f"Similarity: "
          f"{duplicate.highest_similarity:.4f}"
      )

    # -------------------------------------------
    # 5. Persist transaction 
    # -------------------------------------------

    try:
      for embedding in embeddings:
      
        embedding_bytes = (
          serialize_embedding(
            embedding
          )
        )
  
        self.embedding_repository.create(
          employee_id=employee_id,
          embedding=embedding_bytes,
          model_name=model_name,
          embedding_dimension=(
            EMBEDDING_DIMENSION
          )
        )
      self.session.commit()

    except Exception:
      self.session.rollback()
      raise

    return FaceEnrollmentResult(
        employee_id=employee_id,
        embeddings_saved=len(
            embeddings
        ),
        minimum_similarity=(
            validation.minimum_similarity
        ),
        maximum_similarity=(
            validation.maximum_similarity
        ),
        average_similarity=(
            validation.average_similarity
        ),
    )

  def delete_by_employee_id(
      self,
      employee_id: int
  ) -> None:

    statement = delete(
      FaceEmbedding
    ).where(
      FaceEmbedding.employee_id 
      == employee_id
    )

    self.session.execute(
      statement
    )
  