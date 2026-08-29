from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class EmployeeCreate(BaseModel):

    employee_code: str = Field(
        min_length=1,
        max_length=50,
    )

    name: str = Field(
        min_length=1,
        max_length=150,
    )

    email: EmailStr | None = None

    department: str | None = Field(
        default=None,
        max_length=100,
    )

    designation: str | None = Field(
        default=None,
        max_length=100,
    )


class EmployeeUpdate(BaseModel):

    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=150,
    )

    email: EmailStr | None = None

    department: str | None = Field(
        default=None,
        max_length=100,
    )

    designation: str | None = Field(
        default=None,
        max_length=100,
    )

    is_active: bool | None = None


class EmployeeResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
    employee_code: str
    name: str
    email: str | None
    department: str | None
    designation: str | None
    is_active: bool
    created_at: datetime