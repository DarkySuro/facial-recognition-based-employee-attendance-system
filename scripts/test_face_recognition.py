from datetime import date

import cv2
import numpy as np

from backend.app.ai.face_engine import FaceEngine
from backend.app.db.database import SessionLocal
from backend.app.services.recognition_service import (
    RecognitionService,
)
from backend.app.ai.recognition_stabilizer import (
    RecognitionStabilizer,
)
from backend.app.ai.face_tracker import (
    FaceTracker,
)
from backend.app.ai.recognition_stabilizer import (
    RecognitionStabilizer,
)
from backend.app.services.attendance_service import (
    AttendanceService
)


def main():

    print("Initializing FaceEngine...")

    face_engine = FaceEngine()

    session = SessionLocal()

    recognition_service = RecognitionService(
        session=session,
        recognition_threshold=0.70,
    )

    attendance_service = AttendanceService(
        session
    )

    tracker = FaceTracker(
        max_distance=100.0,
        max_missed_frames=10,
    )

    stabilizers = {}

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

    attendance_processed_tracks = set()
    attendance_processing_date = date.today()

    try:

        while True:

            current_date = date.today()

            if current_date != attendance_processing_date:

                attendance_processed_tracks.clear()
                attendance_processing_date = current_date

            success, frame = camera.read()

            if not success:

                print(
                    "Could not read camera frame."
                )

                break

            faces = face_engine.detect(
                frame
            )

            tracked_faces = tracker.update(
                faces
            )

            visible_track_ids = (
                track_id for track_id, _ in tracked_faces
            )

            attendance_processed_tracks.intersection_update(
                visible_track_ids
            )

            active_track_ids = {
                track_id
                for track_id, _ in tracked_faces
            }

            stabilizers = {
                track_id: stabilizer
                for track_id, stabilizer in stabilizers.items()
                if track_id in active_track_ids
            }

            # if len(faces) == 1:
            #     embedding = faces[0].embedding
            #     print(
            #         "LIVE EMBEDDING:",
            #         "shape =", embedding.shape,
            #         "dtype =", embedding.dtype,
            #         "norm =", np.linalg.norm(embedding),
            #     )

            for track_id, face in tracked_faces:

                if track_id not in stabilizers:

                    stabilizers[track_id] = (
                        RecognitionStabilizer(
                            required_matches=3,
                            history_size=5,
                        )
                    )

                x1, y1, x2, y2 = (
                    face.bbox.astype(int)
                )

                embedding = face_engine.get_embedding(face)

                result = (
                    recognition_service.recognize(
                        embedding
                    )
                )

                stable_result = stabilizers[track_id].update(
                        employee_id=result.employee_id,
                        similarity=result.similarity,
                    )

                attendance_result = None

                if (
                    stable_result.confirmed
                    and track_id
                    not in attendance_processed_tracks
                ):
                    attendance_result = (
                        attendance_service.mark_attendance(
                            employee_id=(
                                stable_result.employee_id
                            ),
                            recognition_confidence=(
                                stable_result.similarity
                            )
                        )
                    )

                    attendance_processed_tracks.add(
                        track_id
                    )

                if stable_result.confirmed:

                    if attendance_result is not None:

                        if attendance_result.attendance_marked:

                            attendance_status = (
                                "ATTENDANCE MARKED"
                            )

                        elif attendance_result.already_marked:

                            attendance_status = (
                                "ALREADY MARKED"
                            )

                        else:

                            attendance_status = (
                                "PROCESSED"
                            )

                    else:

                        attendance_status = (
                            "CONFIRMED"
                        )

                    label = (
                        f"Track {track_id} | "
                        f"Employee {stable_result.employee_id} | "
                        f"{stable_result.similarity:.2f} | "
                        f"CONFIRMED"
                    )

                elif result.recognized:

                    label = (
                        f"Track {track_id} | "
                        f"Employee {result.employee_id} | "
                        f"{result.similarity:.2f} | "
                        F"CANDIDATE"
                    )

                else:

                    label = (
                        F"Track {track_id} | "
                        f"UNKNOWN | "
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