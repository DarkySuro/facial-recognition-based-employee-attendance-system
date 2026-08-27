import numpy as np


EMBEDDING_DIMENSION = 512


def serialize_embedding(
    embedding: np.ndarray,
) -> bytes:
    embedding = np.asarray(
        embedding,
        dtype=np.float32,
    )

    if embedding.shape != (
        EMBEDDING_DIMENSION,
    ):
        raise ValueError(
            f"Expected embedding shape "
            f"({EMBEDDING_DIMENSION},), "
            f"got {embedding.shape}"
        )

    return embedding.tobytes()


def deserialize_embedding(
    data: bytes,
) -> np.ndarray:

    embedding = np.frombuffer(
        data,
        dtype=np.float32,
    )

    if embedding.shape != (
        EMBEDDING_DIMENSION,
    ):
        raise ValueError(
            f"Expected embedding shape "
            f"({EMBEDDING_DIMENSION},), "
            f"got {embedding.shape}"
        )

    return embedding.copy()