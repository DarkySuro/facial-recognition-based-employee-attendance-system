import cv2
import numpy as np

from backend.app.ai.face_engine import FaceEngine

def main():
  engine = FaceEngine()

  camera = cv2.VideoCapture(
    0,
    cv2.CAP_DSHOW,
  )

  if not camera.isOpened():
    print("Could not open camera!")
    return

  print("Camera started...")
  print("Look at the camera!")
  print("Press Q to exit")

  while True:
    success, frame = camera.read()

    if not success:
      break

    faces = engine.detect(frame)

    for face in faces:
      embedding = engine.get_embedding(face)

      print("Embedding shape:", embedding.shape)
      print("Embedding dtype:", embedding.dtype)
      print("Embedding norm:", np.linalg.norm(embedding))

      camera.release()
      cv2.destroyAllWindows()

      return

    cv2.imshow(
      "Embedding Test", 
      frame
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
      break

  camera.release()
  cv2.destroyAllWindows()

if __name__ == "__main__":
  main()