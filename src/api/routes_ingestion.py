from src.ingestion.zeek_conn_parser import parse_zeek_conn_log
from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
import uuid
import os

from src.db.session import get_db
from src.db.models import IngestionRun

router = APIRouter(prefix="/ingestion", tags=["ingestion"])


UPLOAD_DIR = "uploads"


@router.post("/upload")
def upload_log_file(
    file: UploadFile = File(...),
    log_type: str = "zeek_conn",
    db: Session = Depends(get_db)
):
    # 1. создаем ingestion run
    run = IngestionRun(
        source_type=log_type,
        source_name=file.filename,
        status="pending",
        records_ingested=0
    )

    db.add(run)
    db.commit()
    db.refresh(run)

    # 2. сохраняем файл
    file_id = str(run.id)
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}_{file.filename}")

    with open(file_path, "wb") as f:
        content = file.file.read()
        f.write(content)

    # 3. обновляем статус
    run.status = "completed"
    db.commit()

    return {
        "ingestion_run_id": str(run.id),
        "filename": file.filename,
        "status": run.status
    }

@router.get("/parse-test/{ingestion_run_id}")
def parse_test_ingestion_run(ingestion_run_id: str, db: Session = Depends(get_db)):
    run = db.query(IngestionRun).filter(IngestionRun.id == ingestion_run_id).first()

    if not run:
        return {"error": "ingestion run not found"}

    file_path = os.path.join(UPLOAD_DIR, f"{run.id}_{run.source_name}")

    records = parse_zeek_conn_log(file_path)

    return {
        "ingestion_run_id": str(run.id),
        "filename": run.source_name,
        "records_found": len(records),
        "sample": records[:3]
    }
