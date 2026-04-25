from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from app.models.base import Base

class Quiz(Base):
    __tablename__ = "quiz"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    answers = Column(JSONB, nullable=False, server_default='[]')
