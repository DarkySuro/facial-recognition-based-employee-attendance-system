import cv2
import numpy as np

from backend.app.ai.face_engine import FaceEngine
from backend.app.ai.quality import FaceQualityChecker
from backend.app.services.enrollment_service import (
    EnrollmentService,
)
from backend.app.ai.enrollment_validator import (
    EnrollmentValidator,
)   


REQUIRED_SAMPLES = 5
MINIMUM_ENROLLMENT_SIMILARITY = 0.65


def main():

    engine = FaceEngine()

    quality_checker = (
        FaceQualityChecker()
    )

    enrollment_service = (
        EnrollmentService(
            face_engine=engine,
            quality_checker=quality_checker,
            required_samples=REQUIRED_SAMPLES,
        )
    )

    validator = EnrollmentValidator(
        minimum_similarity_threshold=(
            MINIMUM_ENROLLMENT_SIMILARITY
        )
    )

    camera = cv2.VideoCapture(
        0,
        cv2.CAP_DSHOW,
    )

    if not camera.isOpened():
        print("Could not open camera.")
        return

    embeddings = []

    print()
    print("=" * 50)
    print("FACE ENROLLMENT TEST")
    print("=" * 50)
    print()
    print(
        f"Required samples: {REQUIRED_SAMPLES}"
    )
    print("Look at the camera.")
    print("Press SPACE to capture.")
    print("Press Q to cancel.")
    print()

    while True:

        success, frame = camera.read()

        if not success:
            print(
                "Could not read camera frame."
            )
            break

        faces = engine.detect(frame)

        if len(faces) == 1:

            face = faces[0]

            x1, y1, x2, y2 = (
                face.bbox.astype(int)
            )

            quality = (
                quality_checker.validate(
                    face
                )
            )

            if quality.valid:
                status = (
                    "READY - Press SPACE"
                )
            else:
                status = (
                    f"NOT READY: "
                    f"{quality.reason}"
                )

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2,
            )

        elif len(faces) == 0:

            status = "NO FACE DETECTED"

        else:

            status = (
                "MULTIPLE FACES - "
                "Only one allowed"
            )

        cv2.putText(
            frame,
            status,
            (20, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (0, 255, 0),
            2,
        )

        cv2.putText(
            frame,
            f"Samples: "
            f"{len(embeddings)}/"
            f"{REQUIRED_SAMPLES}",
            (20, 70),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (0, 255, 0),
            2,
        )

        cv2.imshow(
            "Employee Enrollment",
            frame,
        )

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            print(
                "Enrollment cancelled."
            )
            break

        if key == 32:  # SPACE

            embedding, reason = (
                enrollment_service.process_frame(
                    frame
                )
            )

            if embedding is None:

                print(
                    f"Sample rejected: "
                    f"{reason}"
                )

                continue

            embeddings.append(
                embedding
            )

            print(
                f"Sample "
                f"{len(embeddings)}/"
                f"{REQUIRED_SAMPLES} "
                f"captured."
            )

            if (
                len(embeddings)
                >= REQUIRED_SAMPLES
            ):  
                print()
                print(
                    "Enrollment capture "
                    "complete."
                )

                break

    camera.release()
    cv2.destroyAllWindows()

    if len(embeddings) == REQUIRED_SAMPLES:


        result = validator.validate(embeddings)
        
        print()
        print("=" * 50)
        print("ENROLLMENT SUCCESS")
        print("=" * 50)

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

        if result.valid:

            print()
            print("✅ ENROLLMENT VALIDATED")

            for index, embedding in enumerate(
                embeddings,
                start=1,
            ):
                print(
                    f"Embedding {index}: "
                    f"shape={embedding.shape}, "
                    f"norm={np.linalg.norm(embedding):.6f}"
                )

        else:

            print()
            print("❌ ENROLLMENT REJECTED")
            print(result.reason)
    else:

        print(
            f"Enrollment incomplete. "
            f"Captured "
            f"{len(embeddings)}/"
            f"{REQUIRED_SAMPLES} samples."
        )


if __name__ == "__main__":
    main()