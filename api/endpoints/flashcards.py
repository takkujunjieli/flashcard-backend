from fastapi import APIRouter
from core.database import get_db_connection
from models.flashcard import Flashcard

router = APIRouter()

@router.get("/flashcards/")
async def get_flashcards():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, question, answer, terminology, keywords FROM flashcards")
    rows = cursor.fetchall()
    conn.close()

    flashcards = [{"id": r["id"], "question": r["question"], "answer": r["answer"], "terminology": r["terminology"].split(","), "keywords": r["keywords"].split(",")} for r in rows]
    return {"flashcards": flashcards}

@router.get("/flashcards/search/")
async def search_flashcards(term: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, question, answer, terminology, keywords FROM flashcards WHERE terminology LIKE ? OR keywords LIKE ?", (f"%{term}%", f"%{term}%"))
    rows = cursor.fetchall()
    conn.close()

    flashcards = [{"id": r["id"], "question": r["question"], "answer": r["answer"], "terminology": r["terminology"].split(","), "keywords": r["keywords"].split(",")} for r in rows]
    return {"flashcards": flashcards}

@router.delete("/flashcards/{flashcard_id}")
async def delete_flashcard(flashcard_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM flashcards WHERE id = ?", (flashcard_id,))
    conn.commit()
    conn.close()
    return {"message": "Flashcard deleted"}