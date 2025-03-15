from fastapi import APIRouter, UploadFile, File
import shutil
from pathlib import Path
from services.text_processing import extract_text

router = APIRouter()

UPLOAD_FOLDER = Path("./uploads")
UPLOAD_FOLDER.mkdir(exist_ok=True)

@router.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    file_path = UPLOAD_FOLDER / file.filename
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    text = extract_text(file_path)
    return {"filename": file.filename, "extracted_text": text[:500]}  # Preview text
