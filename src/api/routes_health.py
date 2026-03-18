from fastapi import APIRouter
from sqlalchemy import text
from src.db.session import engine

router = APIRouter()


@router.get("/health")
def health_check():
    db_status = "unknown"

    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"

    return {
        "status": "ok",
        "service": "ai-network-anomaly-detector",
        "database": db_status
    }
