from typing import List
from pydantic import BaseModel
import os

class Settings(BaseModel):
    PROJECT_NAME: str = "Small Shop Sales Pattern Analysis"
    VERSION: str = "1.0.0"
    API_PREFIX: str = "/api"
    BACKEND_HOST: str = os.getenv("BACKEND_HOST", "127.0.0.1")
    BACKEND_PORT: int = int(os.getenv("BACKEND_PORT", "8000"))
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "*"
    ]
    MAX_UPLOAD_SIZE_MB: int = 50

settings = Settings()
