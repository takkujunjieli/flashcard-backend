from pydantic import BaseModel
from typing import List

class Flashcard(BaseModel):
  id: int
  section: str
  question: str
  answer: str
  terminology: List[str]
