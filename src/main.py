from src.api.routes_ingestion import router as ingestion_router
from fastapi import FastAPI
from src.config import settings
from src.api.routes_health import router as health_router
from src.db.base import Base
from src.db.session import engine
import src.db.models  # noqa: F401

app = FastAPI(title=settings.app_name)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


app.include_router(health_router)
app.include_router(ingestion_router)
