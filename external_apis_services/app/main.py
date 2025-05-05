from fastapi import FastAPI
from .routes import location_routes

app = FastAPI()
app.include_router(location_routes.router)
