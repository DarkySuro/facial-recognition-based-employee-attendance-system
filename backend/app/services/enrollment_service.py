from dataclasses import dataclass

import numpy as np

from backend.app.ai.embedding import (
    serialize_embedding,
)
from backend.app.ai.face_engine import FaceEngine
from backend.app.ai.quality import (
    FaceQualityChecker,
)


@dataclass
class EnrollmentResult:
    success: bool
    embeddings: list[np.ndarray]
    reason: str | None = None


class EnrollmentService:

    def __init__(
        self,
        face_engine: FaceEngine,
        quality_checker: FaceQualityChecker,
        required_samples: int = 5,
    ):
        self.face_engine = face_engine
        self.quality_checker = (
            quality_checker
        )
        self.required_samples = (
            required_samples
        )

    def process_frame(
        self,
        frame,
    ):

        faces = self.face_engine.detect(
            frame
        )

        if len(faces) == 0:
            return None, (
                "No face detected."
            )

        if len(faces) > 1:
            return None, (
                "Multiple faces detected. "
                "Only one person should be "
                "present during enrollment."
            )

        face = faces[0]

        quality = (
            self.quality_checker.validate(
                face
            )
        )

        if not quality.valid:
            return None, quality.reason

        embedding = (
            self.face_engine.get_embedding(
                face
            )
        )

        return embedding, None