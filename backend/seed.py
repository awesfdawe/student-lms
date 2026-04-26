import asyncio
import json
import os
import sys
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import text

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app.core.config import settings

database_url = str(settings.sqlalchemy_database_uri)
engine = create_async_engine(database_url)
SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

async def seed():
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "data.json")
    if not os.path.exists(data_path):
        data_path = os.path.join(os.path.dirname(__file__), "..", "data.json")
        if not os.path.exists(data_path): return
    with open(data_path, "r", encoding="utf-8") as f: data = json.load(f)

    async with SessionLocal() as session:
        async with session.begin():
            singleton_mapping = {"globals": "globals", "landing_page": "landing_page", "privacy_policy": "privacy", "terms_of_service": "terms", "login": "login", "register": "register", "not_found": "not_found"}
            for json_key, table_name in singleton_mapping.items():
                if json_key in data and data[json_key]:
                    try: await session.execute(text(f"TRUNCATE TABLE {table_name} CASCADE"))
                    except: pass
                    item = data[json_key]
                    processed = {}
                    vals_list = []
                    for k, v in item.items():
                        if isinstance(v, (dict, list)):
                            processed[k] = json.dumps(v, ensure_ascii=False)
                            vals_list.append(f"CAST(:{k} AS jsonb)")
                        else:
                            processed[k] = v
                            vals_list.append(f":{k}")
                    cols, vals = ", ".join(processed.keys()), ", ".join(vals_list)
                    await session.execute(text(f"INSERT INTO {table_name} ({cols}) VALUES ({vals})"), processed)

            for table in ["pages", "faqs", "courses", "quiz", "ui_dictionary"]:
                if table in data and data[table]:
                    try: await session.execute(text(f"TRUNCATE TABLE {table} CASCADE"))
                    except: pass
                    for item in data[table]:
                        processed = {}
                        vals_list = []
                        for k, v in item.items():
                            if isinstance(v, (dict, list)):
                                processed[k] = json.dumps(v, ensure_ascii=False)
                                vals_list.append(f"CAST(:{k} AS jsonb)")
                            else:
                                processed[k] = v
                                vals_list.append(f":{k}")
                        cols, vals = ", ".join(processed.keys()), ", ".join(vals_list)
                        await session.execute(text(f"INSERT INTO {table} ({cols}) VALUES ({vals})"), processed)
if __name__ == "__main__":
    asyncio.run(seed())
