from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.db.models.face_embedding import FaceEmbedding


class FaceEmbeddingRepository:

    def __init__(self, session: Session):
        self.session = session

    def create(
        self,
        employee_id: int,
        embedding: bytes,
        model_name: str,
        embedding_dimension: int,
    ) -> FaceEmbedding:

        face_embedding = FaceEmbedding(
            employee_id=employee_id,
            embedding=embedding,
            model_name=model_name,
            embedding_dimension=embedding_dimension,
        )

        self.session.add(face_embedding)

        return face_embedding

    def get_by_employee_id(
        self,
        employee_id: int,
    ) -> list[FaceEmbedding]:

        statement = select(
            FaceEmbedding
        ).where(
            FaceEmbedding.employee_id
            == employee_id
        )

        return list(
            self.session.scalars(statement)
        )

    def get_all(self) -> list[FaceEmbedding]:

        statement = select(
            FaceEmbedding
        )

        return list(
            self.session.scalars(statement)
        )