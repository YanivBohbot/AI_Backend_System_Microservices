from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime


class LogEntry(BaseModel):
    timestamp: datetime
    service: str
    event: str
    input: Optional[Dict] = None
    output: Optional[Dict] = None
    message: Optional[str] = None
