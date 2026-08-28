from dataclasses import dataclass

import numpy as np

from backend.app.ai.embedding import (
  deserialize_embedding
)

from backend.app.ai.similarity import (
  cosine_similarity
)

@dataclass
class DuplicateCheckResult:
  is_duplicate: bool
  matched_employee_id: int | None
  highest_similarity: float

class DuplicateDetector:

  def __init__(
    self,
    threshold: float = 0.70,
  ):
    self.threshold = threshold

  def check(
    self,
    new_embeddings: list[np.ndarray],
    existing_embeddings,  
  ) -> DuplicateCheckResult:
    
    highest_similarity = -1.0
    matched_employee_id = None

    for existing in existing_embeddings:
      stored_embedding = (
        deserialize_embedding(
          existing.embedding
        )
      )

      for new_embedding in new_embeddings:
        similarity = (
          cosine_similarity(
            new_embedding,
            stored_embedding
          )
        )

        if similarity > highest_similarity:
          highest_similarity = similarity

          matched_employee_id = (
            existing.employee_id
          )

    is_duplicate = (
      matched_employee_id is not None 
      and highest_similarity 
      >= self.threshold
    )

    if not is_duplicate:
      matched_employee_id = None

    return DuplicateCheckResult(
      is_duplicate=is_duplicate,
      matched_employee_id=matched_employee_id,
      highest_similarity=highest_similarity
    )