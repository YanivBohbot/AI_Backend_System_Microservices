from typing import List

from fastapi import APIRouter, Depends, status

from ..models import LogEntry
from ..services.logger_service import LogService

router = APIRouter(prefix="/logs")


@router.post("/", status_code=status.HTTP_201_CREATED)
def ingest_log(log: LogEntry, log_service: LogService = Depends()):
    log_service.save_log(log)
    return {"status": "logged"}


@router.get("/", response_model=List[LogEntry])
def list_logs(log_service: LogService = Depends()):
    return log_service.get_logs()
