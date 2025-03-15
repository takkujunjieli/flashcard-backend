# app/api/__init__.py
from fastapi import APIRouter
from app.api.endpoints import upload, flashcards, inference

api_router = APIRouter()
api_router.include_router(upload.router, prefix="/upload", tags=["Upload"])
api_router.include_router(flashcards.router, prefix="/flashcards", tags=["Flashcards"])
api_router.include_router(inference.router, prefix="/inference", tags=["Inference"])
