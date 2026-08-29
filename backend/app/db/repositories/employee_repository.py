from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.db.models.employee import Employee

class EmployeeRepository:

  def __init__(
      self,
      session: Session
  ):
    self.session = session

  # ------------------------------------------
  # Get employee by ID
  # ------------------------------------------
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

  # ------------------------------------------
  # Get employee by employee_code
  # ------------------------------------------
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

  # ------------------------------------------
  # Get employee by email
  # ------------------------------------------
  def get_by_email(
      self,
      email: str
  ) -> Employee | None:
    statement = select(
      Employee
    ).where(
      Employee.email == email
    )

    return self.session.scalar(statement)

  # ------------------------------------------
  # Get all employees
  # ------------------------------------------
  def get_all(
      self,
      active_only: bool = False,
  ) -> list[Employee]:

    statement = select(
      Employee
    )

    if active_only:
      statement = select(
        Employee.is_active.is_(True)
      )

    statement = statement.order_by(
      Employee.id
    )

    return list(
      self.session.scalars(statement)
    )

  # ------------------------------------------
  # Create employee 
  # ------------------------------------------
  def create(
      self,
      employee_code: str,
      name: str,
      email: str | None = None,
      department: str | None = None,
      designation: str | None = None,
  ) -> Employee:
    employee = Employee(
      employee_code=employee_code,
      name=name,
      email=email,
      department=department,
      designation=designation,
      is_active=True
    )

    self.session.add(employee)

    return employee

  # ------------------------------------------
  # Update employee
  # ------------------------------------------
  def update(
      self,
      employee: Employee,
      name: str | None = None,
      email: str | None = None,
      department: str | None = None,
      designation: str | None = None,
      is_active: bool | None = None
  ) -> Employee:

    if name is not None:
      employee.name = name

    if email is not None:
      employee.email = email

    if department is not None:
      employee.designation = department

    if designation is not None:
      employee.designation = designation

    if is_active is not None:
      employee.is_active = is_active

    return employee