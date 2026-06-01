from fastapi import FastAPI
from app.routes import log_routes
from .services.logger_service import LogService
import os

app = FastAPI()


log_service = LogService(bucket_name="bucket_log")


@app.on_event("startup")
def startup():
    print("Log Service started with S3 integration")


# Dependency injection
def get_log_service():
    return log_service


app.include_router(log_routes.router)
