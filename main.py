from fastapi import FastAPI
from api.endpoints import upload, flashcards, inference
from core.database import init_db

app = FastAPI()

app.include_router(upload.router, prefix="/api")
app.include_router(flashcards.router, prefix="/api")
app.include_router(inference.router, prefix="/api")

init_db()
