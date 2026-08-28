from collections import deque
from dataclasses import dataclass


@dataclass
class StabilizedRecognition:
    employee_id: int | None
    similarity: float
    confirmed: bool


class RecognitionStabilizer:

    def __init__(
        self,
        required_matches: int = 3,
        history_size: int = 5,
    ):
        self.required_matches = required_matches

        self.history = deque(
            maxlen=history_size
        )

    def update(
        self,
        employee_id: int | None,
        similarity: float,
    ) -> StabilizedRecognition:

        self.history.append(
            (
                employee_id,
                similarity,
            )
        )

        if employee_id is None:

            return StabilizedRecognition(
                employee_id=None,
                similarity=similarity,
                confirmed=False,
            )

        matching_results = [
            result
            for result in self.history
            if result[0] == employee_id
        ]

        if len(matching_results) < self.required_matches:

            return StabilizedRecognition(
                employee_id=employee_id,
                similarity=similarity,
                confirmed=False,
            )

        average_similarity = (
            sum(
                result[1]
                for result in matching_results
            )
            / len(matching_results)
        )

        return StabilizedRecognition(
            employee_id=employee_id,
            similarity=average_similarity,
            confirmed=True,
        )

    def reset(self) -> None:

        self.history.clear()