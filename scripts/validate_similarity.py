from pathlib import Path

import cv2
import numpy as np

from backend.app.ai.face_engine import FaceEngine
from backend.app.ai.similarity import cosine_similarity


IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
}


def get_embedding(
    engine: FaceEngine,
    image_path: Path,
) -> np.ndarray | None:

    image = cv2.imread(str(image_path))

    if image is None:
        print(f"[ERROR] Could not read: {image_path}")
        return None

    print(
        f"[IMAGE] {image_path.name} "
        f"shape={image.shape} "
        f"dtype={image.dtype}"
    )

    faces = engine.detect(image)

    print(
        f"[DETECTION] {image_path.name}: "
        f"{len(faces)} face(s)"
    )

    if len(faces) == 0:
        print(
            f"[WARNING] No face detected: "
            f"{image_path}"
        )
        return None

    if len(faces) > 1:
        print(
            f"[WARNING] Multiple faces detected: "
            f"{image_path}"
        )

    face = max(
        faces,
        key=lambda f: (
            f.bbox[2] - f.bbox[0]
        ) * (
            f.bbox[3] - f.bbox[1]
        ),
    )

    return engine.get_embedding(face)


def load_person_embeddings(
    engine: FaceEngine,
    person_dir: Path,
) -> list[np.ndarray]:

    embeddings = []

    for image_path in sorted(
        person_dir.iterdir()
    ):
        if image_path.suffix.lower() not in IMAGE_EXTENSIONS:
            continue

        embedding = get_embedding(
            engine,
            image_path,
        )

        if embedding is not None:
            embeddings.append(embedding)

    return embeddings


def main():

    base_dir = Path(
        "data/face_validation"
    )

    if not base_dir.exists():
        print(
            f"Directory not found: {base_dir}"
        )
        return

    person_dirs = [
        directory
        for directory in base_dir.iterdir()
        if directory.is_dir()
    ]

    if len(person_dirs) < 2:
        print(
            "Add at least two people "
            "for similarity validation."
        )
        return

    print("Initializing FaceEngine...")

    engine = FaceEngine()

    embeddings_by_person = {}

    for person_dir in person_dirs:

        print(
            f"\nProcessing: {person_dir.name}"
        )

        embeddings = load_person_embeddings(
            engine,
            person_dir,
        )

        embeddings_by_person[
            person_dir.name
        ] = embeddings

        print(
            f"Valid embeddings: {len(embeddings)}"
        )

    print("\n" + "=" * 60)
    print("SAME-PERSON SIMILARITY")
    print("=" * 60)

    for person, embeddings in (
        embeddings_by_person.items()
    ):

        for i in range(len(embeddings)):
            for j in range(
                i + 1,
                len(embeddings),
            ):

                similarity = cosine_similarity(
                    embeddings[i],
                    embeddings[j],
                )

                print(
                    f"{person}: "
                    f"{i + 1} vs {j + 1} "
                    f"→ {similarity:.4f}"
                )

    print("\n" + "=" * 60)
    print("DIFFERENT-PERSON SIMILARITY")
    print("=" * 60)

    person_names = list(
        embeddings_by_person.keys()
    )

    for i in range(len(person_names)):
        for j in range(
            i + 1,
            len(person_names),
        ):

            person_a = person_names[i]
            person_b = person_names[j]

            for embedding_a in embeddings_by_person[
                person_a
            ]:

                for embedding_b in embeddings_by_person[
                    person_b
                ]:

                    similarity = cosine_similarity(
                        embedding_a,
                        embedding_b,
                    )

                    print(
                        f"{person_a} vs "
                        f"{person_b} "
                        f"→ {similarity:.4f}"
                    )


if __name__ == "__main__":
    main()