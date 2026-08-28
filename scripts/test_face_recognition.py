import cv2
import numpy as np

from backend.app.ai.face_engine import FaceEngine
from backend.app.db.database import SessionLocal
from backend.app.services.recognition_service import (
    RecognitionService,
)


def main():

    print("Initializing FaceEngine...")

    face_engine = FaceEngine()

    session = SessionLocal()

    recognition_service = RecognitionService(
        session=session,
        recognition_threshold=0.70,
    )

    camera = cv2.VideoCapture(
        0,
        cv2.CAP_DSHOW,
    )

    if not camera.isOpened():

        print(
            "Could not open camera."
        )

        session.close()

        return

    print()
    print("Camera started.")
    print("Look at the camera.")
    print("Press Q to exit.")

    try:

        while True:

            success, frame = camera.read()

            if not success:

                print(
                    "Could not read camera frame."
                )

                break

            faces = face_engine.detect(
                frame
            )

            if len(faces) == 1:
                embedding = faces[0].embedding
                print(
                    "LIVE EMBEDDING:",
                    "shape =", embedding.shape,
                    "dtype =", embedding.dtype,
                    "norm =", np.linalg.norm(embedding),
                )

            for face in faces:

                x1, y1, x2, y2 = (
                    face.bbox.astype(int)
                )

                embedding = face_engine.get_embedding(face)

                result = (
                    recognition_service.recognize(
                        face.embedding
                    )
                )

                if result.recognized:

                    label = (
                        f"Employee "
                        f"{result.employee_id} "
                        f""
                        f"{result.similarity:.2f}"
                    )

                else:

                    label = (
                        f"UNKNOWN "
                        f"{result.similarity:.2f}"
                    )

                cv2.rectangle(
                    frame,
                    (x1, y1),
                    (x2, y2),
                    (0, 255, 0),
                    2,
                )

                cv2.putText(
                    frame,
                    label,
                    (x1, max(y1 - 10, 20)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 0),
                    2,
                )

            cv2.imshow(
                "Face Recognition",
                frame,
            )

            key = (
                cv2.waitKey(1)
                & 0xFF
            )

            if key == ord("q"):

                break

    finally:

        camera.release()

        cv2.destroyAllWindows()

        session.close()

        print(
            "Recognition system stopped."
        )


if __name__ == "__main__":
    main()