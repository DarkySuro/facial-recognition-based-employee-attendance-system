from dataclasses import dataclass
import numpy as np

from backend.app.ai.similarity import cosine_similarity

@dataclass
class MatchResult:
  matched: bool
  similarity: float
  employee_id: int | None

class FaceMatcher:
  def __init__(
    self,
    threshold: float = 0.45,
  ):
    self.threshold = threshold

  def compare(
    self,
    query_embedding: np.ndarray,
    known_embedding: np.ndarray,
    employee_id: int,
  ) -> MatchResult:
    similarity = cosine_similarity(
      query_embedding,
      known_embedding,
    )

    matched = similarity >= self.threshold

    return MatchResult(
      matched=matched,
      similarity=similarity,
      employee_id=(
        employee_id if matched
        else None
      ),
    )
    