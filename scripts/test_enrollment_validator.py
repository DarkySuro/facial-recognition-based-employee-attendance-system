import numpy as np

from backend.app.ai.enrollment_validator import (
  EnrollmentValidator
)

def main():

  validator = EnrollmentValidator(
    minimum_similarity_threshold=0.65
  )

  # Simulate normalized embeddings
  rng = np.random.default_rng(42)
  base = rng.normal(
    size=512
  ).astype(np.float32)

  base /= np.linalg.norm(base)

  embeddings = []

  for _ in range(5):
    embedding = (
      base +
      rng.normal(
        scale=0.02,
        size=512,
      )
    ).astype(np.float32)

    embedding /= np.linalg.norm(embedding)
    embeddings.append(embedding)

    result = validator.validate(embedding)

    print()
    print("=" * 50)
    print("ENROLLMENT VALIDATION TEST")
    print("=" * 50)

    print(f"Valid: {result.valid}")

    print(
      f"Minimum similarity: "
      f"{result.minimum_similarity:.4f}"
    )

    print(
        f"Maximum similarity: "
        f"{result.maximum_similarity:.4f}"
    )

    print(
        f"Average similarity: "
        f"{result.average_similarity:.4f}"
    )

    if result.reason:
        print(
            f"Reason: {result.reason}"
        )

if __name__ == "__main__":
  main()