import numpy as np

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session

from backend.app.db.database import get_db

from backend.app.schemas.face_enrollment import (
    FaceEnrollmentRequest,
    FaceEnrollmentResponse,
)

from backend.app.services.face_enrollment_service import (
    FaceEnrollmentService,
)


router = APIRouter(
    prefix="/employees",
    tags=["Face Enrollment"],
)


@router.post(
    "/{employee_id}/face-enrollment",
    response_model=FaceEnrollmentResponse,
    status_code=status.HTTP_201_CREATED,
)
def enroll_face(
    employee_id: int,
    payload: FaceEnrollmentRequest,
    db: Session = Depends(get_db),
):

    service = FaceEnrollmentService(
        db
    )

    embeddings = [
        np.asarray(
            embedding,
            dtype=np.float32,
        )
        for embedding in payload.embeddings
    ]

    try:

        result = service.enroll(
            employee_id=employee_id,
            embeddings=embeddings,
            model_name=payload.model_name,
        )

        return FaceEnrollmentResponse(
            employee_id=result.employee_id,
            embeddings_saved=(
                result.embeddings_saved
            ),
            minimum_similarity=(
                result.minimum_similarity
            ),
            maximum_similarity=(
                result.maximum_similarity
            ),
            average_similarity=(
                result.average_similarity
            ),
        )

    except ValueError as error:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        )