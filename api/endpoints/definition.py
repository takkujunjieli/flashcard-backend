from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.llm_inference import efficient_definition_generation
# from core.database import get_db_connection
from models.flashcard import Flashcard

router = APIRouter()


class FlashcardRequest(BaseModel):
    filename: str
    userPrompt: str


@router.post("/generate_definitions/", response_model=list[Flashcard])
async def generate_definitions(request: FlashcardRequest):
    """
    Generates flashcards using the pre-processed text file.
    """
    try:
        terminology = request.terminology
        definitions = efficient_definition_generation(
            request.filename, terminology)

        # Check if there was an error in flashcard generation
        if "error" in definitions:
            raise HTTPException(status_code=500, detail=definitions["error"])

        # Convert flashcards to the Flashcard model format
        flashcards_model = [
            Flashcard(
                id=index,  # Increment ID dynamically
                question=definitions["definition"],
                answer=definitions["extension"],
                terminology=[],
                keywords=[]
            )
            for index, definitions in enumerate(definitions)
        ]

        return flashcards_model
    except Exception as e:
        # Log the error (you can use logging module for more advanced logging)
        print(f"Error generating definitions: {e}")
        # Raise an HTTPException with a detailed error message
        raise HTTPException(
            status_code=500, detail=f"Internal Server Error: {e}")
