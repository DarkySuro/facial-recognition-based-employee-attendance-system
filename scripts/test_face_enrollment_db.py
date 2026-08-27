import numpy as np

from backend.app.ai.face_engine import FaceEngine
from backend.app.ai.quality import FaceQualityChecker
from backend.app.db.database import SessionLocal
from backend.app.services.enrollment_service import (
    EnrollmentService,
)
from backend.app.services.face_enrollment_service import (
    FaceEnrollmentService,
)


EMPLOYEE_ID = 1
REQUIRED_SAMPLES = 5
MOBILE_CAMERA = "http://192.168.0.101:8080/video"

def main():

    # ------------------------------------------
    # Initialize AI components
    # ------------------------------------------

    face_engine = FaceEngine()

    quality_checker = FaceQualityChecker()

    capture_service = EnrollmentService(
        face_engine=face_engine,
        quality_checker=quality_checker,
        required_samples=REQUIRED_SAMPLES,
    )

    # ------------------------------------------
    # Open camera
    # ------------------------------------------

    import cv2

    camera = cv2.VideoCapture(
        MOBILE_CAMERA,
        cv2.CAP_DSHOW,
    )

    if not camera.isOpened():
        print("Could not open camera.")
        return

    embeddings = []

    print(
        f"Capture {REQUIRED_SAMPLES} "
        "face samples."
    )

    print(
        "Press SPACE to capture."
    )

    print(
        "Press Q to cancel."
    )

    while len(embeddings) < REQUIRED_SAMPLES:

        success, frame = camera.read()

        if not success:
            print(
                "Could not read camera frame."
            )
            break
        
        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

        faces = face_engine.detect(frame)

        status = (
            f"Samples: "
            f"{len(embeddings)}/"
            f"{REQUIRED_SAMPLES}"
        )

        if len(faces) == 1:

            face = faces[0]

            x1, y1, x2, y2 = (
                face.bbox.astype(int)
            )

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2,
            )

            quality = quality_checker.validate(
                face
            )

            if quality.valid:
                status += (
                    " | READY"
                )
            else:
                status += (
                    f" | {quality.reason}"
                )

        elif len(faces) == 0:

            status += (
                " | NO FACE"
            )

        else:

            status += (
                " | MULTIPLE FACES"
            )

        cv2.putText(
            frame,
            status,
            (20, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2,
        )

        cv2.imshow(
            "Face Enrollment",
            frame,
        )

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):

            print(
                "Enrollment cancelled."
            )

            break

        if key == 32:

            embedding, reason = (
                capture_service.process_frame(
                    frame
                )
            )

            if embedding is None:

                print(
                    f"Rejected: {reason}"
                )

                continue

            embeddings.append(
                embedding
            )

            print(
                f"Captured "
                f"{len(embeddings)}/"
                f"{REQUIRED_SAMPLES}"
            )

    camera.release()
    cv2.destroyAllWindows()

    # ------------------------------------------
    # Stop if incomplete
    # ------------------------------------------

    if len(embeddings) != REQUIRED_SAMPLES:

        print(
            "Enrollment incomplete."
        )

        return

    # ------------------------------------------
    # Save to database
    # ------------------------------------------

    session = SessionLocal()

    try:

        enrollment_service = (
            FaceEnrollmentService(
                session
            )
        )

        result = (
            enrollment_service.enroll(
                employee_id=EMPLOYEE_ID,
                embeddings=embeddings,
            )
        )

        print()
        print("=" * 50)
        print("FACE ENROLLMENT SUCCESS")
        print("=" * 50)

        print(
            f"Employee ID: "
            f"{result.employee_id}"
        )

        print(
            f"Embeddings saved: "
            f"{result.embeddings_saved}"
        )

        print(
            f"Minimum similarity: "
            f"{result.minimum_similarity:.4f}"
        )

        print(
            f"Average similarity: "
            f"{result.average_similarity:.4f}"
        )

        print(
            f"Maximum similarity: "
            f"{result.maximum_similarity:.4f}"
        )

    except Exception as error:

        print()
        print(
            "ENROLLMENT FAILED"
        )

        print(
            f"Error: {error}"
        )

    finally:

        session.close()


if __name__ == "__main__":
    main()