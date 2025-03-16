from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.llm_inference import efficient_flashcard_generation
# from core.database import get_db_connection
from models.flashcard import Flashcard

router = APIRouter()


class FlashcardRequest(BaseModel):
    filename: str


@router.post("/generate_flashcards/", response_model=list[Flashcard])
async def generate_flashcards(request: FlashcardRequest):
    """
    Generates flashcards using the pre-processed text file.
    """
    try:

        flashcards = efficient_flashcard_generation(request.filename)

        # Check if there was an error in flashcard generation
        if "error" in flashcards:
            raise HTTPException(status_code=500, detail=flashcards["error"])

        # Store the generated flashcards in the database
        # conn = get_db_connection()
        # cursor = conn.cursor()
        # for flashcard in flashcards:
        #     cursor.execute(
        #         "INSERT INTO flashcards (question, answer, terminology, keywords) VALUES (?, ?, ?, ?)",
        #         (flashcard["question"], flashcard["answer"], ",".join(flashcard["terminology"]), ",".join(flashcard["keywords"]))
        #     )
        # conn.commit()
        # conn.close()

        # Convert flashcards to the Flashcard model format
        flashcards_model = [Flashcard(
            id=None,  # Assuming the ID is auto-generated by the database
            question=flashcard["question"],
            answer=flashcard["answer"],
            terminology=flashcard["terminology"],
            keywords=flashcard["keywords"]
        ) for flashcard in flashcards]

        return flashcards_model
    except Exception as e:
        # Log the error (you can use logging module for more advanced logging)
        print(f"Error generating flashcards: {e}")
        # Raise an HTTPException with a detailed error message
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")
