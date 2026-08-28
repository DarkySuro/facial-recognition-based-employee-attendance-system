import numpy as np

from backend.app.ai.duplicate_detector import (
    DuplicateDetector,
)


def normalize(vector):
    vector = vector.astype(
        np.float32
    )

    return vector / np.linalg.norm(
        vector
    )


def main():

    rng = np.random.default_rng(42)

    base = normalize(
        rng.normal(
            size=512
        )
    )

    similar = normalize(
        base
        + rng.normal(
            scale=0.02,
            size=512,
        )
    )

    different = normalize(
        rng.normal(
            size=512
        )
    )

    detector = DuplicateDetector(
        threshold=0.70
    )

    # Fake database records
    class FakeEmbedding:
        def __init__(
            self,
            employee_id,
            embedding,
        ):
            self.employee_id = employee_id
            self.embedding = embedding.tobytes()

    existing = [
        FakeEmbedding(
            employee_id=101,
            embedding=base,
        )
    ]

    result = detector.check(
        new_embeddings=[similar],
        existing_embeddings=existing,
    )

    print(
        "Similar person:"
    )

    print(
        f"Duplicate: "
        f"{result.is_duplicate}"
    )

    print(
        f"Employee: "
        f"{result.matched_employee_id}"
    )

    print(
        f"Similarity: "
        f"{result.highest_similarity:.4f}"
    )

    result = detector.check(
        new_embeddings=[different],
        existing_embeddings=existing,
    )

    print()
    print(
        "Different person:"
    )

    print(
        f"Duplicate: "
        f"{result.is_duplicate}"
    )

    print(
        f"Employee: "
        f"{result.matched_employee_id}"
    )

    print(
        f"Similarity: "
        f"{result.highest_similarity:.4f}"
    )


if __name__ == "__main__":
    main()