from fastapi import APIRouter
from backend.app.api.v1.employees import (
  router as employee_router
)
from backend.app.api.v1.cameras import (
  router as camera_router
)
from backend.app.api.v1.attendance import (
  router as attendance_router
)

router = APIRouter(
    prefix="/api/v1",
)

router.include_router(  
  employee_router,
)

router.include_router(
  camera_router,
)

router.include_router(
  attendance_router,
)

@router.get("/health")
def api_health_check():

  return {
    "status": "ok",
    "api_version": "v1",
  }