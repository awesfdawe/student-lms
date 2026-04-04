from sqlalchemy import Column, Integer, String, Text
from app.models.base import Base

class GlobalSettings(Base):
    __tablename__ = "globals"

    id = Column(Integer, primary_key=True, index=True)
    phone = Column(String(255))
    email = Column(String(255))
    office_address = Column(String(255))

class LandingPage(Base):
    __tablename__ = "landing_page"

    id = Column(Integer, primary_key=True, index=True)
    hero_title = Column(String(255))
    hero_subtitle = Column(Text)
