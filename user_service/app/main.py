from fastapi import FastAPI
from .routes import user_routes
from database.database import Base, engine

# Create DB tables
Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(user_routes.router, prefix="/user")


@app.get("/")
async def root():
    return {"message": "user is running"}
