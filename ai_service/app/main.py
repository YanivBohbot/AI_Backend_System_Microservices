from fastapi import FastAPI
from .routes import predict_routes

app = FastAPI()
app.include_router(predict_routes.router, prefix="/fraud", tags=["Fraud Detection"])
