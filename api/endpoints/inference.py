from fastapi import APIRouter
from services.llm_inference import efficient_flashcard_generation

router = APIRouter()

@router.post("/generate_flashcards/")
async def generate_flashcards(filename: str):
    """
    Generates flashcards using the pre-processed text file.
    """
    flashcards = efficient_flashcard_generation(filename)
    
    return {"flashcards": flashcards}

