from sqlalchemy.orm import Session

from backend.app.ai.recognition import FaceRecognizer
from backend.app.core.config import settings
from backend.app.db.repositories.face_embedding_repository import FaceEmbeddingRepository

class RecognitionService:

    def __init__(
        self,
        session: Session,
        recognition_threshold: float | None = None,
    ):

        self.embedding_repository = FaceEmbeddingRepository(    session
        )

        threshold = (
            recognition_threshold
            if recognition_threshold is not None
            else settings.face_recognition_threshold
        )

        self.recognizer = FaceRecognizer(
            threshold=recognition_threshold
        )

    def recognize(
        self,
        embedding,
    ):

        stored_embeddings = (
            self.embedding_repository.get_all_active(exclude_employee_id=None)
        )

        return self.recognizer.recognize(
            embedding=embedding,
            stored_embeddings=stored_embeddings,
        )