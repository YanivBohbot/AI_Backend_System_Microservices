from fastapi import FastAPI
from app.routes import log_routes

app = FastAPI()

app.include_router(log_routes.router)
