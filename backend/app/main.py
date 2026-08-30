from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
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

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    components = schema.get("components", {}).get("schemas", {})

    for component in components.values():

        properties = component.get("properties", {})

        for property_schema in properties.values():

            # Handle array of uploaded files
            if (
                property_schema.get("type") == "array"
                and isinstance(
                    property_schema.get("items"),
                    dict,
                )
            ):
                items = property_schema["items"]

                if (
                    items.get("contentMediaType")
                    == "application/octet-stream"
                ):
                    items.pop(
                        "contentMediaType",
                        None,
                    )

                    items["format"] = "binary"

            # Handle single uploaded file
            elif (
                property_schema.get("type") == "string"
                and property_schema.get(
                    "contentMediaType"
                )
                == "application/octet-stream"
            ):
                property_schema.pop(
                    "contentMediaType",
                    None,
                )

                property_schema["format"] = "binary"

    app.openapi_schema = schema

    return app.openapi_schema


app.openapi = custom_openapi

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

