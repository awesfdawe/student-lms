import json
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import SessionLocal
from app.models.globals import GlobalSettings, LandingPage
from app.models.faq import FAQ
from app.models.dictionary import UIDictionary
from app.models.course import Course

def seed():
    db = SessionLocal()
    
    data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "data.json")
    
    if not os.path.exists(data_path):
        print(f"File not found: {data_path}")
        return

    with open(data_path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            print("Invalid JSON")
            return

    if not db.query(GlobalSettings).first() and "globals" in data:
        g = data["globals"]
        db.add(GlobalSettings(
            phone=g.get("phone", ""),
            email=g.get("email", ""),
            office_address=g.get("office_address", "")
        ))

    if not db.query(LandingPage).first() and "landing_page" in data:
        lp = data["landing_page"]
        db.add(LandingPage(
            hero_title=lp.get("hero_title") or lp.get("hero_main_text", ""),
            hero_subtitle=lp.get("hero_subtitle") or lp.get("hero_highlight", "")
        ))

    if not db.query(Course).first() and "courses" in data:
        for c in data["courses"]:
            db.add(Course(
                slug=c.get("slug", "default-slug"),
                title=c.get("title", ""),
                duration=c.get("duration", ""),
                feature=c.get("feature", ""),
                description=c.get("description", ""),
                price=int(c.get("price", 0)),
                image_path=c.get("image_path", "")
            ))

    if not db.query(FAQ).first() and "faq" in data:
        for item in data["faq"]:
            db.add(FAQ(
                question=item.get("question", ""),
                answer=item.get("answer", "")
            ))

    if not db.query(UIDictionary).first():
        if isinstance(data, list):
            dict_items = [i for i in data if "key" in i and "value" in i]
        else:
            dict_items = data.get("ui_dictionary", [])
            
        for item in dict_items:
            db.add(UIDictionary(
                key=item.get("key", ""),
                value=item.get("value", "")
            ))

    db.commit()
    db.close()
    print("Database seeded successfully.")

if __name__ == "__main__":
    seed()
