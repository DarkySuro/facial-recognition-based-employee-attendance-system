from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from urllib.parse import quote_plus


class Settings(BaseSettings):
    app_name: str = Field(
        default="Facial Recognition Based Attendance System",
        validation_alias="APP_NAME",
    )

    app_env: str = Field(
        default="development",
        validation_alias="APP_ENV",
    )

    debug: bool = Field(
        default=True,
        validation_alias="DEBUG",
    )

    mysql_host: str = Field(
        default="localhost",
        validation_alias="MYSQL_HOST",
    )

    mysql_port: int = Field(
        default=3306,
        validation_alias="MYSQL_PORT",
    )

    mysql_user: str = Field(
        default="root",
        validation_alias="MYSQL_USER",
    )

    mysql_password: str = Field(
        validation_alias="MYSQL_PASSWORD",
    )

    mysql_database: str = Field(
        default="face_attendance",
        validation_alias="MYSQL_DATABASE",
    )

    face_recognition_threshold: float = Field(
        default=0.45,
        validation_alias="FACE_RECOGNITION_THRESHOLD",
    )

    camera_index: int = Field(
        default=0,
        validation_alias="CAMERA_INDEX",
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def database_url(self) -> str:
        password = quote_plus(self.mysql_password)

        return (
            f"mysql+pymysql://"
            f"{self.mysql_user}:"
            f"{password}@"
            f"{self.mysql_host}:"
            f"{self.mysql_port}/"
            f"{self.mysql_database}"
        )


settings = Settings()