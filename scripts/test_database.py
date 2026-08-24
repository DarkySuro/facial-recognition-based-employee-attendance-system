from sqlalchemy import text

from backend.app.db.database import engine


def main():
    try:
        with engine.connect() as connection:
            result = connection.execute(
                text("SELECT VERSION()")
            )

            version = result.scalar()

            print("MySQL connection successful.")
            print(f"MySQL version: {version}")

    except Exception as error:
        print("MySQL connection failed.")
        print(f"Error: {error}")


if __name__ == "__main__":
    main()