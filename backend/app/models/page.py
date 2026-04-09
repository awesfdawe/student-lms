from sqlalchemy import Column, Integer, String, Text
from app.models.base import Base

class Page(Base):
    __tablename__ = "pages"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String(255), unique=True, index=True, nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(Text)
    additional_content = Column(Text, nullable=True)
