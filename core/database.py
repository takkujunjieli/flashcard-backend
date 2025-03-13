import sqlite3

DB_FILE = "flashcards.db"

def init_db():
  conn = sqlite3.connect(DB_FILE)
  cursor = conn.cursor()
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS flashcards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            section TEXT,
            question TEXT,
            answer TEXT,
            terminology TEXT
        )
    """)
  conn.commit()
  conn.close()

def save_flashcard(section, question, answer, terminology):
  conn = sqlite3.connect(DB_FILE)
  cursor = conn.cursor()
  cursor.execute("INSERT INTO flashcards (section, question, answer, terminology) VALUES (?, ?, ?, ?)",
                 (section, question, answer, ",".join(terminology)))
  conn.commit()
  conn.close()
