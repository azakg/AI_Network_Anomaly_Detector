from fastapi import FastAPI
from src.config import settings
from src.api.routes_health import router as health_router

app = FastAPI(title=settings.app_name)

app.include_router(health_router)
