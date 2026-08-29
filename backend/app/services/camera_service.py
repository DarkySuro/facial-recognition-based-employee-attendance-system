from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from backend.app.db.models.camera import Camera
from backend.app.db.repositories.camera_repository import (
    CameraRepository,
)


class CameraService:

    def __init__(
        self,
        session: Session,
    ):
        self.session = session

        self.repository = CameraRepository(
            session
        )

    # ------------------------------------------
    # Get camera
    # ------------------------------------------

    def get_camera(
        self,
        camera_id: int,
    ) -> Camera:

        camera = self.repository.get_by_id(
            camera_id
        )

        if camera is None:

            raise ValueError(
                f"Camera {camera_id} not found."
            )

        return camera

    # ------------------------------------------
    # Get all cameras
    # ------------------------------------------

    def get_cameras(
        self,
        active_only: bool = False,
    ) -> list[Camera]:

        return self.repository.get_all(
            active_only=active_only
        )

    # ------------------------------------------
    # Create camera
    # ------------------------------------------

    def create_camera(
        self,
        camera_code: str,
        name: str,
        source: str,
        location: str | None = None,
    ) -> Camera:

        existing_camera = (
            self.repository.get_by_camera_code(
                camera_code
            )
        )

        if existing_camera is not None:

            raise ValueError(
                "Camera code already exists."
            )

        try:

            camera = self.repository.create(
                camera_code=camera_code,
                name=name,
                source=source,
                location=location,
            )

            self.session.commit()

            self.session.refresh(
                camera
            )

            return camera

        except IntegrityError:

            self.session.rollback()

            raise ValueError(
                "Camera could not be created "
                "because a unique constraint "
                "was violated."
            )

    # ------------------------------------------
    # Update camera
    # ------------------------------------------

    def update_camera(
        self,
        camera_id: int,
        name: str | None = None,
        source: str | None = None,
        location: str | None = None,
        is_active: bool | None = None,
    ) -> Camera:

        camera = self.get_camera(
            camera_id
        )

        try:

            camera = self.repository.update(
                camera=camera,
                name=name,
                source=source,
                location=location,
                is_active=is_active,
            )

            self.session.commit()

            self.session.refresh(
                camera
            )

            return camera

        except IntegrityError:

            self.session.rollback()

            raise ValueError(
                "Camera could not be updated."
            )