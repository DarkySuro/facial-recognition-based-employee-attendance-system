from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from backend.app.db.database import get_db
from backend.app.schemas.employee import (
    EmployeeCreate,
    EmployeeResponse,
    EmployeeUpdate,
)
from backend.app.services.employee_service import (
    EmployeeService,
)


router = APIRouter(
    prefix="/employees",
    tags=["Employees"],
)

@router.post(
  "",
  response_model=EmployeeResponse,
  status_code=status.HTTP_201_CREATED,
)
def create_employee(
  payload: EmployeeCreate,
  db: Session = Depends(get_db),
):
  service = EmployeeService(db)
  try:
    return service.create_employee(
      employee_code=payload.employee_code,
      name=payload.name,
      email=(
        str(payload.email)
        if payload.email is not None
        else None
      ),
      department=payload.department,
      designation=payload.designation
    )
  
  except ValueError as error:
    raise HTTPException(
      status_code=status.HTTP_409_CONFLICT,
      detail=str(error),
    )

@router.get(
  "/{employee_id}",
  response_model=EmployeeResponse,
)
def get_employee(
  employee_id: int,
  db: Session = Depends(get_db),
):

  service = EmployeeService(db)
  try:
    return service.get_employee(
      employee_id=employee_id
    )
  except ValueError as error:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      details=str(error)
    )

@router.get(
  "",
  response_model=list[EmployeeResponse]
)
def get_employees(
  active_only: bool = Query(
    default=False
  ),
  db: Session = Depends(get_db)
):
  service = EmployeeService(db)
  return service.get_employees(
    active_only=active_only
  )

@router.patch(
  "/{employee_id}",
  response_model=EmployeeResponse,
)
def update_employee(
  employee_id: int,
  payload: EmployeeUpdate,
  db: Session = Depends(get_db)
):
  service = EmployeeService(db)
  try:
    return service.update_employee(
      employee_id=employee_id,
      name=payload.name,
      email=(
        str(payload.email)
        if payload.email is not None
        else None
      ),
      department=payload.department,
      designation=payload.designation,
      is_active=payload.is_active
    )
  except ValueError as error:
    message = str(error)
    if "not found" in message.lower():
      raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=message
      )
    raise HTTPException(
      status_code=status.HTTP_409_CONFLICT,
      detail=message
    )