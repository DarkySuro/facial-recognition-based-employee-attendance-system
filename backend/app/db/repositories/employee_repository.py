from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.db.models.employee import Employee

class EmployeeRepository:

  def __init__(
      self,
      session: Session
  ):
    self.session = session

  def get_by_id(
      self,
      employee_id: int
  ) -> Employee | None:
    statement = select(
      Employee
    ).where(
      Employee.id == employee_id
    )

    return self.session.scalar(statement)

  def get_by_employee_code(
      self,
      employee_code: str
  ) -> Employee | None:

    statement = select(
      Employee
    ).where(
      Employee.employee_code
      == employee_code
    )

    return self.session.scalar(statement)