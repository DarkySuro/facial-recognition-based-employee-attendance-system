from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from backend.app.db.models.employee import Employee
from backend.app.db.repositories.employee_repository import (
    EmployeeRepository,
)


class EmployeeService:

    def __init__(
        self,
        session: Session,
    ):
        self.session = session

        self.repository = EmployeeRepository(
            session
        )

    # ------------------------------------------
    # Get employee
    # ------------------------------------------

    def get_employee(
        self,
        employee_id: int,
    ) -> Employee:

        employee = self.repository.get_by_id(
            employee_id
        )

        if employee is None:

            raise ValueError(
                f"Employee {employee_id} "
                "not found."
            )

        return employee

    # ------------------------------------------
    # Get employees
    # ------------------------------------------

    def get_employees(
        self,
        active_only: bool = False,
    ) -> list[Employee]:

        return self.repository.get_all(
            active_only=active_only
        )

    # ------------------------------------------
    # Create employee
    # ------------------------------------------

    def create_employee(
        self,
        employee_code: str,
        name: str,
        email: str | None = None,
        department: str | None = None,
        designation: str | None = None,
    ) -> Employee:

        existing_code = (
            self.repository
            .get_by_employee_code(
                employee_code
            )
        )

        if existing_code is not None:

            raise ValueError(
                "Employee code already exists."
            )

        if email is not None:

            existing_email = (
                self.repository
                .get_by_email(email)
            )

            if existing_email is not None:

                raise ValueError(
                    "Employee email already exists."
                )

        try:

            employee = (
                self.repository.create(
                    employee_code=employee_code,
                    name=name,
                    email=email,
                    department=department,
                    designation=designation,
                )
            )

            self.session.commit()

            self.session.refresh(
                employee
            )

            return employee

        except IntegrityError:

            self.session.rollback()

            raise ValueError(
                "Employee could not be created "
                "because a unique constraint was "
                "violated."
            )

    # ------------------------------------------
    # Update employee
    # ------------------------------------------

    def update_employee(
        self,
        employee_id: int,
        name: str | None = None,
        email: str | None = None,
        department: str | None = None,
        designation: str | None = None,
        is_active: bool | None = None,
    ) -> Employee:

        employee = self.get_employee(
            employee_id
        )

        if email is not None:

            existing_email = (
                self.repository
                .get_by_email(email)
            )

            if (
                existing_email is not None
                and existing_email.id
                != employee_id
            ):

                raise ValueError(
                    "Employee email already exists."
                )

        try:

            employee = (
                self.repository.update(
                    employee=employee,
                    name=name,
                    email=email,
                    department=department,
                    designation=designation,
                    is_active=is_active,
                )
            )

            self.session.commit()

            self.session.refresh(
                employee
            )

            return employee

        except IntegrityError:

            self.session.rollback()

            raise ValueError(
                "Employee could not be updated."
            )