from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.core.config import settings
from backend.app.api.v1.router import router as api_router

app = FastAPI(
  title=settings.app_name,
  version="0.1.0",
  description=(
    "AI-powered employee attendance system "
    "using facial recognition"
  ),
)

app.add_middleware(
  CORSMiddleware,
  allow_origins=[
    "http://localhost:5173",
    "http://127.0.0.1:5173"
  ],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

@app.get("/")
def root():
  return {
    "application": settings.app_name,
    "status": "running",
    "environment": settings.app_env,
  }

app.include_router(
  api_router
)

@app.get("/health")
def health():
  return {
    "status": "healthy",
    "service": "face-attendance-system",
  }

