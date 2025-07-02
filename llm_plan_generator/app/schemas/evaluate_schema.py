from pydantic import BaseModel
from typing import List, Dict

class Question(BaseModel):
    question: str
    answer: str

class EvaluateInput(BaseModel):
    questions: List[Question]
    answers: List[str]
