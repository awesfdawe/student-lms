from sqlalchemy import Column, Integer, String, Text, Boolean
from app.models.base import Base

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String(255), unique=True, index=True, nullable=False)
    title = Column(String(255), nullable=False)
    duration = Column(String(255))
    feature = Column(String(255))
    description = Column(Text)
    price = Column(Integer, default=0)
    is_free = Column(Boolean, default=False)
    image_path = Column(String(255))
