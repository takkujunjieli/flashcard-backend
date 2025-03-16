from pydantic import BaseModel
from typing import List, Optional

class Flashcard(BaseModel):
    id: Optional[int]
    question: str
    answer: str
    terminology: List[str]
    keywords: List[str]
