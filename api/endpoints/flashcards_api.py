from fastapi import APIRouter
from app.core.database import get_db_connection
from app.models.flashcard import Flashcard

router = APIRouter()

@router.get("/flashcards/")
async def get_flashcards():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, section, question, answer, terminology FROM flashcards")
    rows = cursor.fetchall()
    conn.close()

    flashcards = [{"id": r[0], "section": r[1], "question": r[2], "answer": r[3], "terminology": r[4].split(",")} for r in rows]
    return {"flashcards": flashcards}

@router.delete("/flashcards/{flashcard_id}")
async def delete_flashcard(flashcard_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM flashcards WHERE id = ?", (flashcard_id,))
    conn.commit()
    conn.close()
    return {"message": "Flashcard deleted"}