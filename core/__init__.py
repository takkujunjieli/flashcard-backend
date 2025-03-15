# app/core/__init__.py
from .database import init_db

# Initialize database at import
init_db()
