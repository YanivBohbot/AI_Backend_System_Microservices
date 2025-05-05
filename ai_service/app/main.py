from fastapi import FastAPI
from app.routes import prediction_routes

app = FastAPI()
app.include_router(prediction_routes.router, prefix="/fraud", tags=["Fraud Detection"])
