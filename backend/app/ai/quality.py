from dataclasses import dataclass

import numpy as np


@dataclass
class FaceQualityResult:
    valid: bool
    reason: str | None = None


class FaceQualityChecker:

    def __init__(
        self,
        min_detection_score: float = 0.70,
        min_face_size: int = 80,
    ):
        self.min_detection_score = (
            min_detection_score
        )
        self.min_face_size = min_face_size

    def validate(
        self,
        face,
    ) -> FaceQualityResult:

        detection_score = float(
            face.det_score
        )

        if (
            detection_score
            < self.min_detection_score
        ):
            return FaceQualityResult(
                valid=False,
                reason=(
                    "Face detection confidence "
                    "is too low."
                ),
            )

        x1, y1, x2, y2 = (
            face.bbox.astype(int)
        )

        width = x2 - x1
        height = y2 - y1

        if (
            width < self.min_face_size
            or height < self.min_face_size
        ):
            return FaceQualityResult(
                valid=False,
                reason=(
                    "Face is too small."
                ),
            )

        return FaceQualityResult(
            valid=True
        )