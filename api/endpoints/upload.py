from fastapi import APIRouter, UploadFile, File, HTTPException
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
    try:
        file_path = UPLOAD_FOLDER / file.filename
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        print(f"File uploaded successfully: {file_path}")

        structured_data = preprocess_text(file_path)

        processed_file_path = PROCESSED_FOLDER / f"{file.filename}.json"
        with open(processed_file_path, "w", encoding="utf-8") as f:
            json.dump(structured_data, f)

        print(f"Structured data saved successfully: {processed_file_path}")

        # Return structured preview
        return {"filename": file.filename, "structured_data": structured_data}
    except Exception as e:
        # Log the error for debugging
        print(f"Error uploading file: {e}")
        raise HTTPException(
            status_code=500, detail=f"Internal Server Error: {e}"
        )
