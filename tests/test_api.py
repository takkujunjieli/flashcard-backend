import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import pytest
from fastapi.testclient import TestClient
from api.endpoints.upload import router as upload_router
from api.endpoints.inference import router as inference_router
from api.endpoints.flashcards import router as flashcards_router
from fastapi import FastAPI
from core.database import init_db

app = FastAPI()
app.include_router(upload_router, prefix="/api")
app.include_router(inference_router, prefix="/api")
app.include_router(flashcards_router, prefix="/api")

client = TestClient(app)

init_db()

pdf_path = Path(__file__).parent / "MMT.pdf"


def test_upload_file():
    print(f"Testing upload_file with path: {pdf_path}")
    with open(pdf_path, "rb") as file:
        response = client.post("/api/upload/", files={"file": file})
    assert response.status_code == 200
    assert "filename" in response.json()
    assert "extracted_text" in response.json()

def test_generate_flashcards():
    print(f"Testing generate_flashcards with path: {pdf_path}")
    with open(pdf_path, "rb") as file:
        response = client.post("/api/generate_flashcards/", files={"file": file})
    assert response.status_code == 200
    assert "flashcards" in response.json()

def test_get_flashcards():
    response = client.get("/api/flashcards/")
    assert response.status_code == 200
    assert "flashcards" in response.json()

def test_search_flashcards():
    response = client.get("/api/flashcards/search/", params={"term": "MMT"})
    assert response.status_code == 200
    assert "flashcards" in response.json()

def test_delete_flashcard():
    # First, add a flashcard to delete
    print(f"Testing delete_flashcard with path: {pdf_path}")
    with open(pdf_path, "rb") as file:
        client.post("/api/generate_flashcards/", files={"file": file})
    
    # Get the flashcards to find the ID of the one to delete
    response = client.get("/api/flashcards/")
    flashcards = response.json()["flashcards"]
    if flashcards:
        flashcard_id = flashcards[0]["id"]
        delete_response = client.delete(f"/api/flashcards/{flashcard_id}")
        assert delete_response.status_code == 200
        assert delete_response.json() == {"message": "Flashcard deleted"}