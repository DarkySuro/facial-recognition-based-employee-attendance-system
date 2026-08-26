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
      print("Could not read camera frame.")
      break

    faces = engine.detect(frame)

    if len(faces) > 0:
      face = faces[0]

      raw_embedding = np.asarray(
        face.embedding,
        dtype=np.float32
      )

      normalized_embedding = engine.get_embedding(face)

      print("Raw Embedding shape:", raw_embedding.shape)
      print("Raw Embedding dtype:", raw_embedding.dtype)
      print("Raw Embedding norm:", np.linalg.norm(raw_embedding))
      print("Normalized embedding shape:", normalized_embedding.shape)
      print("Normalized embedding dtype:", normalized_embedding.dtype)
      print("Normalized embedding norm:", np.linalg.norm(normalized_embedding))

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