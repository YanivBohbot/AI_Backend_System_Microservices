import logging
from typing import List, Optional

from app.models import LogEntry

logger = logging.getLogger("log-service")
logging.basicConfig(
    level=logging.INFO, format="[%(levelname)s] %(asctime)s - %(message)s"
)


class LogService:
    """Stores structured log entries.

    Persistence is in-memory for now (a class-level list shared across instances, since
    FastAPI builds a fresh LogService per request). To move to S3, provision a bucket and
    replace the `_store.append` call with an `s3.put_object` write — the original boto3
    sketch is preserved in git history.
    """

    _store: List[LogEntry] = []

    def __init__(self, bucket_name: Optional[str] = None):
        self.bucket_name = bucket_name

    def save_log(self, loginput: LogEntry) -> None:
        LogService._store.append(loginput)
        logger.info("[%s] %s - %s", loginput.service, loginput.event, loginput.message)

    def get_logs(self) -> List[LogEntry]:
        return list(LogService._store)
