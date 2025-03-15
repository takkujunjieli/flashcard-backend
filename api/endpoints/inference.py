from fastapi import APIRouter, UploadFile, File
import shutil
from pathlib import Path
from services.llama_inference import efficient_flashcard_generation

router = APIRouter()

UPLOAD_FOLDER = Path("./uploads")
UPLOAD_FOLDER.mkdir(exist_ok=True)

@router.post("/generate_flashcards/")
async def generate_flashcards(file: UploadFile = File(...)):
    file_path = UPLOAD_FOLDER / file.filename
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    flashcards = efficient_flashcard_generation(file_path)
    
    return {"flashcards": flashcards}

