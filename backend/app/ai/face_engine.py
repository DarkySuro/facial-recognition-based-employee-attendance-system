import insightface
import numpy as np

class FaceEngine:
  def __init__(
      self,
      model_name: str = 'buffalo_l',
      det_size: tuple[int, int] = (640, 640)
  ):
    self.model = insightface.app.FaceAnalysis(
      name=model_name,
      providers=['CPUExecutionProvider'],
    )

    self.model.prepare(
      ctx_id=0,
      det_size=det_size,
    )

  def detect(self, frame: np.ndarray):
    return self.model.get(frame)

  @staticmethod
  def normalize_embedding(embedding: np.ndarray) -> np.ndarray: 
    embedding = np.asarray(
      embedding,
      dtype=np.float32
    )

    norm = np.linalg.norm(embedding)
    
    if norm == 0:
      raise ValueError(
        "Face embedding has zero magnitude."
    )
    
    return embedding / norm

  def get_embedding(self, face) -> np.ndarray:
    return self.normalize_embedding(face.embedding)