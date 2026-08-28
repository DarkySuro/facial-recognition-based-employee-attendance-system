from dataclasses import dataclass

import numpy as np

from backend.app.ai.embedding import deserialize_embedding
from backend.app.ai.face_engine import FaceEngine
from backend.app.ai.similarity import cosine_similarity


@dataclass
class RecognitionResult:
    employee_id: int | None
    similarity: float
    recognized: bool


class FaceRecognizer:

    def __init__(
        self,
        threshold: float = 0.70,
    ):
        self.threshold = threshold

    def recognize(
        self,
        embedding: np.ndarray,
        stored_embeddings,
    ) -> RecognitionResult:

        # Always normalize incoming embeddings
        embedding = FaceEngine.normalize_embedding(
            embedding
        )

        if not stored_embeddings:
            return RecognitionResult(
                employee_id=None,
                similarity=0.0,
                recognized=False,
            )

        best_similarity = -1.0
        best_employee_id = None

        for stored in stored_embeddings:

            stored_embedding = (
                deserialize_embedding(
                    stored.embedding
                )
            )

            print(
                "STORED:",
                "shape=", stored_embedding.shape,
                "norm=", np.linalg.norm(stored_embedding),
            )

            similarity = np.dot(
                embedding,
                stored_embedding,
            )

            if similarity > best_similarity:

                best_similarity = similarity

                best_employee_id = (
                    stored.employee_id
                )

        if best_similarity >= self.threshold:

            return RecognitionResult(
                employee_id=best_employee_id,
                similarity=best_similarity,
                recognized=True,
            )

        return RecognitionResult(
            employee_id=None,
            similarity=best_similarity,
            recognized=False,
        )