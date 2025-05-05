from fastapi import APIRouter, status
from ..models import LogEntry
from ..services.logger_service import save_log

router = APIRouter()


@router.post("/log", status_code=status.HTTP_201_CREATED)
def ingest_log(log: LogEntry):
    save_log(log)
    return {"message": "Log received"}
