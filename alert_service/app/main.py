from fastapi import FastAPI
from app.routes.alert_routes import alert_router

app = FastAPI()
app.include_router(alert_router, prefix="/alert", tags=["Alert"])
