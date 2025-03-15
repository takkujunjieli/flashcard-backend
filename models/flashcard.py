from pydantic import BaseModel
from typing import List

class Flashcard(BaseModel):
  id: int
  question: str
  answer: str
  terminology: List[str]
  keywords: List[str]
