import os
from typing import List
from pydantic import BaseModel, field_validator, model_validator

class Settings(BaseModel):
    PROJECT_NAME: str = "Small Shop Sales Pattern Analysis"
    VERSION: str = "1.0.0"
    API_PREFIX: str = "/api"
    ENVIRONMENT: str = "development"
    BACKEND_HOST: str = "127.0.0.1"
    BACKEND_PORT: int = 8000
    MAX_UPLOAD_SIZE_MB: int = 50
    CORS_ORIGINS: List[str] = []

    def __init__(self, **data):
        env_mode = os.getenv("ENVIRONMENT", "development").lower()
        backend_host = os.getenv("BACKEND_HOST", "127.0.0.1")
        backend_port = int(os.getenv("BACKEND_PORT", "8000"))
        max_upload = int(os.getenv("MAX_UPLOAD_SIZE_MB", "50"))
        
        env_cors = os.getenv("CORS_ORIGINS")
        if env_cors:
            origins = [origin.strip() for origin in env_cors.split(",") if origin.strip()]
        else:
            origins = [
                "http://localhost:5173",
                "http://127.0.0.1:5173",
                "http://localhost:3000",
                "http://127.0.0.1:3000",
            ]

        data.setdefault("ENVIRONMENT", env_mode)
        data.setdefault("BACKEND_HOST", backend_host)
        data.setdefault("BACKEND_PORT", backend_port)
        data.setdefault("MAX_UPLOAD_SIZE_MB", max_upload)
        data.setdefault("CORS_ORIGINS", origins)
        super().__init__(**data)

    @model_validator(mode="after")
    def validate_production_cors(self):
        if self.ENVIRONMENT == "production" and "*" in self.CORS_ORIGINS:
            raise ValueError("Wildcard CORS origin '*' is strictly prohibited in production mode.")
        return self

settings = Settings()
