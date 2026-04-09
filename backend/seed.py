import asyncio
import json
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import text
from app.core.config import settings

database_url = str(settings.sqlalchemy_database_uri)
if database_url.startswith("postgresql://"):
    database_url = database_url.replace("postgresql://", "postgresql+asyncpg://")

engine = create_async_engine(database_url)
SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

async def seed():
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "data.json")
    
    if not os.path.exists(data_path):
        data_path = os.path.join(os.path.dirname(__file__), "..", "data.json")
        if not os.path.exists(data_path):
            print(f"Файл не найден: {data_path}")
            return
        
    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    async with SessionLocal() as session:
        singleton_mapping = {
            "globals": "globals",
            "landing_page": "landing_page",
            "privacy_policy": "privacy",
            "terms_of_service": "terms",
            "login": "login",
            "register": "register",
            "not_found": "not_found"
        }

        for json_key, table_name in singleton_mapping.items():
            if json_key in data and data[json_key]:
                try:
                    await session.execute(text(f"TRUNCATE TABLE {table_name} CASCADE"))
                except Exception:
                    pass
                try:
                    item = data[json_key]
                    cols = ", ".join(item.keys())
                    vals = ", ".join([f":{k}" for k in item.keys()])
                    await session.execute(text(f"INSERT INTO {table_name} ({cols}) VALUES ({vals})"), item)
                except Exception as e:
                    print(f"Ошибка в таблице {table_name}: {e}")

        for table in ["pages", "faqs", "courses", "quiz", "ui_dictionary"]:
            if table in data and data[table]:
                try:
                    await session.execute(text(f"TRUNCATE TABLE {table} CASCADE"))
                except Exception:
                    pass
                try:
                    for item in data[table]:
                        processed = {}
                        for k, v in item.items():
                            if isinstance(v, (dict, list)):
                                processed[k] = json.dumps(v, ensure_ascii=False)
                            else:
                                processed[k] = v
                        
                        cols = ", ".join(processed.keys())
                        vals = ", ".join([f":{k}" for k in processed.keys()])
                        await session.execute(text(f"INSERT INTO {table} ({cols}) VALUES ({vals})"), processed)
                except Exception as e:
                    print(f"Ошибка в таблице {table}: {e}")

        await session.commit()
        print("База данных успешно заполнена контентом.")

if __name__ == "__main__":
    asyncio.run(seed())
