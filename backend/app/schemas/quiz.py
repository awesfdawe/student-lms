from pydantic import BaseModel, ConfigDict
from typing import List

class QuizAnswerSchema(BaseModel):
    text: str
    experience_score: int

class QuizResponse(BaseModel):
    id: int
    title: str
    answers: List[QuizAnswerSchema]

    model_config = ConfigDict(from_attributes=True)
