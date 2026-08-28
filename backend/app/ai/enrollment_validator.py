from dataclasses import dataclass

import numpy as np

from backend.app.ai.similarity import cosine_similarity


@dataclass
class EnrollmentValidationResult:
    valid: bool
    minimum_similarity: float
    maximum_similarity: float
    average_similarity: float
    reason: str | None = None


class EnrollmentValidator:
    """
    Validates whether multiple face embeddings captured
    during enrollment are sufficiently consistent.
    """

    def __init__(
        self,
        minimum_similarity_threshold: float = 0.65,
    ):
        self.minimum_similarity_threshold = (
            minimum_similarity_threshold
        )

    def validate(
        self,
        embeddings: list[np.ndarray],
    ) -> EnrollmentValidationResult:

        if len(embeddings) < 2:
            return EnrollmentValidationResult(
                valid=False,
                minimum_similarity=0.0,
                maximum_similarity=0.0,
                average_similarity=0.0,
                reason=(
                    "At least two embeddings "
                    "are required."
                ),
            )

        similarities = []

        for i in range(len(embeddings)):
            for j in range(i + 1, len(embeddings)):

                similarity = cosine_similarity(
                    embeddings[i],
                    embeddings[j],
                )

                similarities.append(similarity)

        minimum_similarity = min(similarities)
        maximum_similarity = max(similarities)
        average_similarity = float(
            np.mean(similarities)
        )

        valid = (
            minimum_similarity
            >= self.minimum_similarity_threshold
        )

        reason = None

        if not valid:
            reason = (
                "Enrollment samples are not "
                "consistent enough. Please "
                "recapture the employee's face."
            )

        return EnrollmentValidationResult(
            valid=valid,
            minimum_similarity=minimum_similarity,
            maximum_similarity=maximum_similarity,
            average_similarity=average_similarity,
            reason=reason,
        )