from sqlalchemy import Column, Integer, String, Text
from app.models.base import Base


class SiteContent(Base):
    __tablename__ = "site_content"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(255), unique=True, index=True, nullable=False)
    value = Column(Text, nullable=True)
    page = Column(String(255), nullable=True)
