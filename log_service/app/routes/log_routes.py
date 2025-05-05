from fastapi import APIRouter, status
from ..models import LogEntry
from ..services.logger_service import LogService

router = APIRouter(prefix="/logs")
log_service = LogService()


@router.post("/", status_code=status.HTTP_201_CREATED)
def ingest_log(log: LogEntry):
    log_service.save_log(log)
    return {"status": "logged"}
