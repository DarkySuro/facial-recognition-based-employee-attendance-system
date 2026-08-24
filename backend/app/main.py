from fastapi import FastAPI
from backend.app.core.config import settings

app = FastAPI(
  title=settings.app_name,
  version="0.1.0",
  description=(
    "AI-powered employee attendance system "
    "using face recognition"
  ),
)

@app.get("/")
def root():
  return {
    "application": settings.app_name,
    "status": "running",
    "environment": settings.app_env,
  }

@app.get("/health")
def health():
  return {
    "status": "healthy",
  }

