from typing import List
import numpy as np
import cv2

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    UploadFile,
    File,
)
from sqlalchemy.orm import Session

from backend.app.ai.face_engine import FaceEngine
from backend.app.ai.quality import FaceQualityChecker

from backend.app.db.database import get_db

from backend.app.schemas.face_enrollment import (
    FaceEnrollmentRequest,
    FaceEnrollmentResponse,
)
from backend.app.services.enrollment_service import EnrollmentService

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

@router.post(
    "/{employee_id}/face-enrollment/images",
    response_model=FaceEnrollmentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def enroll_face_from_images(
    employee_id: int,
    files: List[UploadFile] = File(
            ...,
            description="Upload atleast 5 images"
        ),
    db: Session = Depends(get_db),
):

    # ------------------------------------------
    # Validate number of samples
    # ------------------------------------------

    required_samples = 5

    if len(files) < required_samples:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"At least {required_samples} "
                "face images are required."
            ),
        )


    # ------------------------------------------
    # Initialize AI enrollment pipeline
    # ------------------------------------------

    face_engine = FaceEngine()

    quality_checker = FaceQualityChecker()

    enrollment_service = EnrollmentService(
        face_engine=face_engine,
        quality_checker=quality_checker,
        required_samples=required_samples,
    )

    embeddings = []


    # ------------------------------------------
    # Process uploaded images
    # ------------------------------------------

    for index, file in enumerate(files):

        # Validate content type

        if (
            file.content_type is None
            or not file.content_type.startswith(
                "image/"
            )
        ):

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    f"File {index + 1} "
                    "is not a valid image."
                ),
            )


        image_bytes = await file.read()


        # Convert bytes → NumPy array

        image_array = np.frombuffer(
            image_bytes,
            dtype=np.uint8,
        )


        # Decode image → OpenCV frame

        frame = cv2.imdecode(
            image_array,
            cv2.IMREAD_COLOR,
        )


        if frame is None:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    f"Could not decode image "
                    f"{index + 1}."
                ),
            )


        # --------------------------------------
        # Extract embedding
        # --------------------------------------

        embedding, error = (
            enrollment_service.process_frame(
                frame
            )
        )


        if error is not None:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    f"Image {index + 1}: "
                    f"{error}"
                ),
            )


        embeddings.append(
            embedding
        )


    # ------------------------------------------
    # Persist through existing service
    # ------------------------------------------

    face_enrollment_service = (
        FaceEnrollmentService(
            db
        )
    )


    try:

        result = (
            face_enrollment_service.enroll(
                employee_id=employee_id,
                embeddings=embeddings,
                model_name="buffalo_l",
            )
        )

        return FaceEnrollmentResponse(
            employee_id=result.employee_id,
            embeddings_saved=result.embeddings_saved,
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

    finally:

        for file in files:
            await file.close() 