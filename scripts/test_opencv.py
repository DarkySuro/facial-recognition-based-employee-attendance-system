import cv2
import time


def main():
    print(f"OpenCV version: {cv2.__version__}")
    print("Opening camera...")

    camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not camera.isOpened():
        print("❌ Camera could not be opened.")
        return

    print("✅ Camera opened successfully.")

    time.sleep(2)

    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    print("Starting camera stream...")
    print("Close the camera window or press Q inside the camera window.")

    while True:
        success, frame = camera.read()

        if not success:
            print("❌ Could not read camera frame.")
            break

        cv2.imshow("Face Attendance - Camera Test", frame)

        # Q = quit
        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            print("Q pressed. Closing camera...")
            break

        # ESC = quit
        if key == 27:
            print("ESC pressed. Closing camera...")
            break

    camera.release()
    cv2.destroyAllWindows()

    print("✅ Camera released successfully.")


if __name__ == "__main__":
    main()