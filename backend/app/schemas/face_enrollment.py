from pydantic import (
    BaseModel,
    Field,
)


class FaceEnrollmentRequest(BaseModel):

    embeddings: list[
        list[float]
    ] = Field(
        min_length=1,
    )

    model_name: str = Field(
        default="buffalo_l",
        min_length=1,
        max_length=100,
    )


class FaceEnrollmentResponse(BaseModel):

    employee_id: int

    embeddings_saved: int

    minimum_similarity: float

    maximum_similarity: float

    average_similarity: float