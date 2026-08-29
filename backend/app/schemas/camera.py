from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CameraCreate(BaseModel):

    camera_code: str = Field(
        min_length=1,
        max_length=50,
    )

    name: str = Field(
        min_length=1,
        max_length=100,
    )

    location: str | None = Field(
        default=None,
        max_length=255,
    )

    source: str = Field(
        min_length=1,
        max_length=255,
    )


class CameraUpdate(BaseModel):

    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )

    location: str | None = Field(
        default=None,
        max_length=255,
    )

    source: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
    )

    is_active: bool | None = None


class CameraResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
    camera_code: str
    name: str
    location: str | None
    source: str
    is_active: bool
    created_at: datetime