from typing import List
from app.models import LogEntry
import logging

logger = logging.getLogger("log-service")
logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(asctime)s - %(message)s")

# Simple in-memory store (can replace with DB later)


class LogService:
    def __init__(self):
        self.logs: List[LogEntry] = []

    def save_log(self, log: LogEntry):
        self.logs.append(log)
        logger.info(f"{log.service} | {log.event} | {log.message}")
        print(f"[LOG] [{log.timestamp}] {log.service}: {log.message}", flush=True)
