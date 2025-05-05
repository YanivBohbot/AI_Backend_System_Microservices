from app.models import LogEntry
import logging
import boto3
import json

logger = logging.getLogger("log-service")
logging.basicConfig(
    level=logging.INFO, format="[%(levelname)s] %(asctime)s - %(message)s"
)

# Simple in-memory store (can replace with DB later)


class LogService:
    def __init__(self):
        self.s3 = boto3.client("s3")
        self.bucket_name = "logs"

    def save_log(self, loginput: LogEntry):
        log_data = loginput.model_dump()
        key = f"logs/{loginput.timestamp.strftime('%Y-%m-%dT%H-%M-%S')}_{loginput.service}.json"
        self.s3.put_object(
            Bucket=self.bucket_name,
            Key=key,
            Body=json.dumps(log_data),
            ContentType="application/json",
        )
        print(f"[S3 LOG] Saved to {key}")

        # self.logs.append(log)
        # logger.info(f"{log.service} | {log.event} | {log.message}")
        # print(f"[LOG] [{log.timestamp}] {log.service}: {log.message}", flush=True)
