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
            question TEXT,
            answer TEXT,
            terminology TEXT,
            keywords TEXT
                   
        )
    """)
    conn.commit()
    conn.close()

def save_flashcard(question, answer, terminology, keywords):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO flashcards (question, answer, terminology, keywords) VALUES (?, ?, ?, ?)", 
                   (question, answer, ",".join(terminology), ",".join(keywords)))
    conn.commit()
    conn.close()
