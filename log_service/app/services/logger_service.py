from typing import List
from app.models import LogEntry

# Simple in-memory store (can replace with DB later)
logs: List[LogEntry] = []


def save_log(log: LogEntry):
    logs.append(log)
    print("Log saved:", log.dict())  # Optional debug
