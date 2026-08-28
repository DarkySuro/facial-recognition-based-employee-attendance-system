from sqlalchemy import (
    select, 
    update
)
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
            is_active=True,
        )

        self.session.add(face_embedding)

        return face_embedding

    def get_all_active(
        self,
        exclude_employee_id: int | None
    ) -> list[FaceEmbedding]:

        statement = select(
            FaceEmbedding
        ).where(
            FaceEmbedding.is_active.is_(True)
        )

        if exclude_employee_id is not None:
            statement = statement.where(
                FaceEmbedding.employee_id 
                != exclude_employee_id
            )
        return list(
            self.session.scalars(statement)
        )

    def get_active_by_employee_id(
        self,
        employee_id: int
    ) -> list[FaceEmbedding]:

        statement = select(
            FaceEmbedding
        ).where(
            FaceEmbedding.employee_id
            == employee_id,
            FaceEmbedding.is_active.is_(True)
        )
        
        return list(
            self.session.scalars(statement)
        )

    def deactivate_by_employee_id(
        self,
        employee_id: int
    ) -> None: 

        statement = (
            update(
                FaceEmbedding
            ).where(
                FaceEmbedding.employee_id
                == employee_id,
                FaceEmbedding.is_active.is_(True)
            ).values(
                is_active=False
            )
        )

        self.session.execute(statement)

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

    def get_all(
        self,
        exclude_employee_id: int | None
    ) -> list[FaceEmbedding]:

        statement = select(
            FaceEmbedding
        )

        if exclude_employee_id is not None:
            statement = statement.where(
                FaceEmbedding.employee_id 
                != exclude_employee_id 
            )

        return list(
            self.session.scalars(statement)
        )