from backend.app.db.database import (
    SessionLocal,
)

from backend.app.services.attendance_service import (
    AttendanceService,
)


EMPLOYEE_ID = 1


def main():

    session = SessionLocal()

    try:

        attendance_service = (
            AttendanceService(
                session
            )
        )

        print(
            "Marking attendance..."
        )

        result = (
            attendance_service.mark_attendance(
                employee_id=EMPLOYEE_ID,
                recognition_confidence=0.85,
            )
        )

        print()

        if result.attendance_marked:

            print(
                "ATTENDANCE MARKED"
            )

        elif result.already_marked:

            print(
                "ATTENDANCE ALREADY MARKED"
            )

        print(
            f"Employee ID: "
            f"{result.employee_id}"
        )

        print(
            f"Attendance ID: "
            f"{result.attendance_id}"
        )

        print(
            f"Check-in time: "
            f"{result.check_in_time}"
        )

    except Exception as error:

        print(
            "ATTENDANCE TEST FAILED"
        )

        print(
            f"Error: {error}"
        )

    finally:

        session.close()


if __name__ == "__main__":
    main()