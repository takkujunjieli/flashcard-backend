import sqlite3
from pathlib import Path

DB_FILE = Path("./flashcards.db")

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # Enables column access by name
    return conn

def init_db():
    conn = get_db_connection()
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
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO flashcards (section, question, answer, terminology) VALUES (?, ?, ?, ?)", 
                   (section, question, answer, ",".join(terminology)))
    conn.commit()
    conn.close()
