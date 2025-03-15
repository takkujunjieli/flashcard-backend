from fastapi import APIRouter, UploadFile, File
import shutil
import json
from pathlib import Path
from services.text_processing import preprocess_text

router = APIRouter()

UPLOAD_FOLDER = Path("./uploads")
UPLOAD_FOLDER.mkdir(exist_ok=True)
PROCESSED_FOLDER = Path("./processed")  # New folder to store structured text
PROCESSED_FOLDER.mkdir(exist_ok=True)

@router.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    """
    Handles file upload and extracts structured content.
    Saves structured text for later use.
    """
    file_path = UPLOAD_FOLDER / file.filename
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    structured_data = preprocess_text(file_path)
    
    processed_file_path = PROCESSED_FOLDER / f"{file.filename}.json"
    with open(processed_file_path, "w", encoding="utf-8") as f:
        json.dump(structured_data, f)

    return {"filename": file.filename, "structured_data": structured_data}  # Return structured preview
