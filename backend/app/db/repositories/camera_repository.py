from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.db.models.camera import Camera


class CameraRepository:

    def __init__(
        self,
        session: Session,
    ):
        self.session = session

    # ------------------------------------------
    # Get camera by ID
    # ------------------------------------------

    def get_by_id(
        self,
        camera_id: int,
    ) -> Camera | None:

        statement = select(
            Camera
        ).where(
            Camera.id == camera_id
        )

        return self.session.scalar(
            statement
        )

    # ------------------------------------------
    # Get camera by camera code
    # ------------------------------------------

    def get_by_camera_code(
        self,
        camera_code: str,
    ) -> Camera | None:

        statement = select(
            Camera
        ).where(
            Camera.camera_code == camera_code
        )

        return self.session.scalar(
            statement
        )

    # ------------------------------------------
    # Get all cameras
    # ------------------------------------------

    def get_all(
        self,
        active_only: bool = False,
    ) -> list[Camera]:

        statement = select(
            Camera
        )

        if active_only:

            statement = statement.where(
                Camera.is_active.is_(True)
            )

        statement = statement.order_by(
            Camera.id
        )

        return list(
            self.session.scalars(
                statement
            )
        )

    # ------------------------------------------
    # Create camera
    # ------------------------------------------

    def create(
        self,
        camera_code: str,
        name: str,
        source: str,
        location: str | None = None,
    ) -> Camera:

        camera = Camera(
            camera_code=camera_code,
            name=name,
            source=source,
            location=location,
            is_active=True,
        )

        self.session.add(
            camera
        )

        return camera

    # ------------------------------------------
    # Update camera
    # ------------------------------------------

    def update(
        self,
        camera: Camera,
        name: str | None = None,
        source: str | None = None,
        location: str | None = None,
        is_active: bool | None = None,
    ) -> Camera:

        if name is not None:
            camera.name = name

        if source is not None:
            camera.source = source

        if location is not None:
            camera.location = location

        if is_active is not None:
            camera.is_active = is_active

        return camera