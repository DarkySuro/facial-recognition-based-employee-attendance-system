import cv2
import requests

from backend.app.ai.face_engine import FaceEngine
from backend.app.ai.quality import FaceQualityChecker
from backend.app.services.enrollment_service import (
    EnrollmentService,
)


API_URL = "http://127.0.0.1:8000"

EMPLOYEE_ID = 1

REQUIRED_SAMPLES = 5


def main():

    print("Initializing FaceEngine...")

    face_engine = FaceEngine()

    quality_checker = FaceQualityChecker()

    enrollment_service = EnrollmentService(
        face_engine=face_engine,
        quality_checker=quality_checker,
        required_samples=REQUIRED_SAMPLES,
    )

    camera = cv2.VideoCapture(
        0,
        cv2.CAP_DSHOW,
    )

    if not camera.isOpened():

        print(
            "Could not open camera."
        )

        return

    embeddings = []

    print()
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

    try:

        while len(embeddings) < REQUIRED_SAMPLES:

            success, frame = camera.read()

            if not success:

                print(
                    "Could not read camera frame."
                )

                break

            faces = face_engine.detect(
                frame
            )

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

                quality = (
                    quality_checker.validate(
                        face
                    )
                )

                if quality.valid:

                    status += " | READY"

                else:

                    status += (
                        f" | {quality.reason}"
                    )

                cv2.rectangle(
                    frame,
                    (x1, y1),
                    (x2, y2),
                    (0, 255, 0),
                    2,
                )

            elif len(faces) == 0:

                status += " | NO FACE"

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
                "Face Enrollment Client",
                frame,
            )

            key = (
                cv2.waitKey(1)
                & 0xFF
            )

            if key == ord("q"):

                print(
                    "Enrollment cancelled."
                )

                return

            if key == 32:

                embedding, reason = (
                    enrollment_service
                    .process_frame(frame)
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

    finally:

        camera.release()

        cv2.destroyAllWindows()

    if len(embeddings) != REQUIRED_SAMPLES:

        print(
            "Enrollment incomplete."
        )

        return

    # ------------------------------------------
    # Send embeddings to FastAPI
    # ------------------------------------------

    payload = {
        "embeddings": [
            embedding.tolist()
            for embedding in embeddings
        ],
        "model_name": "buffalo_l",
    }

    endpoint = (
        f"{API_URL}/api/v1/employees/"
        f"{EMPLOYEE_ID}/face-enrollment"
    )

    print()
    print(
        "Sending embeddings to API..."
    )

    try:

        response = requests.post(
            endpoint,
            json=payload,
            timeout=30,
        )

    except requests.RequestException as error:

        print(
            "Could not connect to API:"
        )

        print(error)

        return

    print()
    print(
        f"API Status: "
        f"{response.status_code}"
    )

    try:

        data = response.json()

    except ValueError:

        print(
            "API returned invalid JSON."
        )

        print(
            response.text
        )

        return

    if response.ok:

        print()
        print("=" * 50)
        print(
            "FACE ENROLLMENT SUCCESS"
        )
        print("=" * 50)

        print(
            f"Employee ID: "
            f"{data['employee_id']}"
        )

        print(
            f"Embeddings saved: "
            f"{data['embeddings_saved']}"
        )

        print(
            f"Minimum similarity: "
            f"{data['minimum_similarity']:.4f}"
        )

        print(
            f"Average similarity: "
            f"{data['average_similarity']:.4f}"
        )

        print(
            f"Maximum similarity: "
            f"{data['maximum_similarity']:.4f}"
        )

    else:

        print()
        print(
            "FACE ENROLLMENT FAILED"
        )

        print(
            data.get(
                "detail",
                "Unknown API error.",
            )
        )


if __name__ == "__main__":
    main()