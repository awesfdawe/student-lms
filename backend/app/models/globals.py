from sqlalchemy import Column, Integer, String, Text
from app.models.base import Base

class GlobalSettings(Base):
    __tablename__ = "globals"

    id = Column(Integer, primary_key=True, index=True)
    phone = Column(String(255))
    email = Column(String(255))
    office_address = Column(String(255))
    footer_copyright = Column(String(255))
    footer_description = Column(Text)
    footer_license = Column(String(255))
    cookie_banner_text = Column(Text)
    cookie_banner_btn_accept = Column(String(255))

class LandingPage(Base):
    __tablename__ = "landing_page"

    id = Column(Integer, primary_key=True, index=True)
    hero_highlight = Column(String(255))
    hero_main_text = Column(String(255))
    hero_stat_1_val = Column(String(255))
    hero_stat_1_desc = Column(String(255))
    hero_stat_2_val = Column(String(255))
    hero_stat_2_desc = Column(String(255))
    hero_stat_3_val = Column(String(255))
    hero_stat_3_desc = Column(String(255))
    courses_title = Column(String(255))
    courses_desc_1 = Column(Text)
    courses_desc_2 = Column(Text)
    quiz_start_title = Column(String(255))
    quiz_start_desc = Column(Text)
    quiz_result_title = Column(String(255))
    quiz_result_subtitle = Column(String(255))
