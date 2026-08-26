import numpy as np

def cosine_similarity(
    embedding_a: np.ndarray,
    embedding_b: np.ndarray
) -> float:
  """
  Calculate cosine similarity between two embeddings.

  Both embeddings should be normalized.
  """

  embedding_a = np.asarray(
    embedding_a,
    dtype=np.float32,
  )

  embedding_b = np.asarray(
    embedding_b,
    dtype=np.float32,
  )

  if embedding_a.shape != embedding_b.shape:
    raise ValueError(
      "Embedding dimensions do not match!"
    )

  similarity = np.dot(
    embedding_a,
    embedding_b,
  )

  return float(similarity)