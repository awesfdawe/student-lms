import os
import json
import urllib.request
from urllib.error import HTTPError
from app.models.base import Base
import app.models

DIRECTUS_URL = os.getenv("DIRECTUS_URL", "http://localhost:8055")
ADMIN_EMAIL = os.getenv("DIRECTUS_ADMIN_EMAIL")
ADMIN_PASSWORD = os.getenv("DIRECTUS_ADMIN_PASSWORD")

def make_req(url, data=None, headers=None, method="POST"):
    req_headers = {"Content-Type": "application/json"}
    if headers: req_headers.update(headers)
    req_data = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=req_data, headers=req_headers, method=method)
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except HTTPError as e:
        return json.loads(e.read().decode())

def main():
    print("🔑 Авторизация в Directus...")
    res = make_req(f"{DIRECTUS_URL}/auth/login", {"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD})
    token = res["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Получаем таблицы прямо из метаданных SQLAlchemy
    tables = [t for t in Base.metadata.tables.keys() if not t.startswith("directus_") and t != "alembic_version"]
    
    for table in tables:
        print(f"📌 Tracking collection: {table}...")
        r = make_req(f"{DIRECTUS_URL}/collections", {"collection": table}, headers)
        if "errors" in r:
            msg = r["errors"][0]["message"]
            if "already exists" not in msg:
                print(f"    ❌ Ошибка API: {msg}")
        else:
            print(f"    ✅ Успешно")

if __name__ == "__main__":
    main()
