import cv2

from backend.app.ai.face_engine import FaceEngine


def main():
    print("Initializing face engine...")

    engine = FaceEngine()

    print("Face engine ready.")
    print("Opening camera...")

    camera = cv2.VideoCapture(
        0,
        cv2.CAP_DSHOW,
    )

    if not camera.isOpened():
        print("Could not open camera.")
        return

    print("Camera opened successfully.")
    print("Press Q to exit.")

    while True:
        success, frame = camera.read()

        if not success:
            print("Could not read frame.")
            break

        faces = engine.detect(frame)

        for face in faces:
            x1, y1, x2, y2 = face.bbox.astype(int)

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2,
            )

            confidence = face.det_score

            cv2.putText(
                frame,
                f"Face: {confidence:.2f}",
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2,
            )

        cv2.imshow(
            "Face Detection Test",
            frame,
        )

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()