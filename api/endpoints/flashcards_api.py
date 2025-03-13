@app.get("/flashcards/")
async def get_flashcards():
  conn = sqlite3.connect(DB_FILE)
  cursor = conn.cursor()
  cursor.execute("SELECT id, section, question, answer, terminology FROM flashcards")
  rows = cursor.fetchall()
  conn.close()

  flashcards = [{"id": r[0], "section": r[1], "question": r[2], "answer": r[3], "terminology": r[4].split(",")} for r in rows]
  return {"flashcards": flashcards}

@app.get("/flashcards/search/")
async def search_flashcards(term: str):
  conn = sqlite3.connect(DB_FILE)
  cursor = conn.cursor()
  cursor.execute("SELECT id, section, question, answer, terminology FROM flashcards WHERE terminology LIKE ?", (f"%{term}%",))
  rows = cursor.fetchall()
  conn.close()

  flashcards = [{"id": r[0], "section": r[1], "question": r[2], "answer": r[3], "terminology": r[4].split(",")} for r in rows]
  return {"flashcards": flashcards}

@app.delete("/flashcards/{flashcard_id}")
async def delete_flashcard(flashcard_id: int):
  conn = sqlite3.connect(DB_FILE)
  cursor = conn.cursor()
  cursor.execute("DELETE FROM flashcards WHERE id = ?", (flashcard_id,))
  conn.commit()
  conn.close()
  return {"message": "Flashcard deleted"}
