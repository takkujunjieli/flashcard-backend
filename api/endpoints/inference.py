from fastapi import APIRouter, UploadFile, File
from app.services.text_processing import preprocess_text
from app.services.llm_inference import run_llama3_inference, generate_flashcard_prompt, generate_definition_prompt
from app.core.database import save_flashcard
import shutil
from pathlib import Path

router = APIRouter()

UPLOAD_FOLDER = Path("./uploads")
UPLOAD_FOLDER.mkdir(exist_ok=True)

@router.post("/generate_flashcards/")
async def generate_flashcards(file: UploadFile = File(...)):
    file_path = UPLOAD_FOLDER / file.filename
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    text = extract_text(file_path)
    sections = preprocess_text(text)

    flashcards = []
    for section in sections:
        prompt = generate_flashcard_prompt(section)
        response = run_llama3_inference(prompt)

        # Extract questions and answers
        qa_pairs = response.split("\n")
        for qa in qa_pairs:
            if "Q:" in qa and "A:" in qa:
                question = qa.split("Q:")[1].strip()
                answer = qa.split("A:")[1].strip()
                save_flashcard(section['key_facts'], question, answer, section['terminology'])
                flashcards.append({"question": question, "answer": answer})

    return {"flashcards": flashcards}
