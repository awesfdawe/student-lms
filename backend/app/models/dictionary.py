from sqlalchemy import Column, Integer, String, Text
from app.models.base import Base

class UIDictionary(Base):
    __tablename__ = "ui_dictionary"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(255), unique=True, index=True, nullable=False)
    value = Column(Text, nullable=False)
