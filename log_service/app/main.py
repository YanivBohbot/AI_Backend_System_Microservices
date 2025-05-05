from fastapi import FastAPI
from app.routes import log_routes
from .services.logger_service import LogService
import os

app = FastAPI()

BUCKET_NAME = os.getenv("S3_LOG_BUCKET", "your-default-log-bucket")
log_service = LogService(bucket_name=BUCKET_NAME)


@app.on_event("startup")
def startup():
    print("Log Service started with S3 integration")


# Dependency injection
def get_log_service():
    return log_service


app.include_router(log_routes.router)
