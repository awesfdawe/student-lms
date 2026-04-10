#!/bin/bash

set -a
[ -f backend/.env ] && . backend/.env
set +a

DIRECTUS_URL=${DIRECTUS_URL:-"http://localhost:8055"}

cd backend
uv run alembic upgrade head
cd ..

until $(curl --output /dev/null --silent --head --fail "$DIRECTUS_URL/server/ping"); do
    sleep 5
done

docker compose exec -T directus npx directus schema apply ./directus-schema.yaml --yes

cat << 'EOF' > seed_test_data.py
import asyncio
import httpx
import os

async def main():
    directus_url = os.environ.get("DIRECTUS_URL", "http://localhost:8055")
    email = os.environ.get("DIRECTUS_ADMIN_EMAIL", "admin@example.com")
    password = os.environ.get("DIRECTUS_ADMIN_PASSWORD", "adminpassword")

    async with httpx.AsyncClient() as client:
        login = await client.post(
            f"{directus_url}/auth/login", 
            json={"email": email, "password": password}
        )
        token = login.json()["data"]["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        assets_path = "seed_data/assets"
        if os.path.exists(assets_path):
            for filename in os.listdir(assets_path):
                filepath = os.path.join(assets_path, filename)
                if not os.path.isfile(filepath):
                    continue
                with open(filepath, "rb") as f:
                    await client.post(f"{directus_url}/files", headers=headers, files={"file": (filename, f)})
        
        await client.post(f"{directus_url}/permissions", headers=headers, json={
            "role": None, "collection": "directus_files", "action": "read", "fields": ["*"]
        })

        files_res = await client.get(f"{directus_url}/files", headers=headers)
        for f in files_res.json().get("data", []):
            name = f.get("filename_download", "")
            new_type = None
            if name.endswith(".svg"): new_type = "image/svg+xml"
            elif name.endswith((".jpg", ".jpeg")): new_type = "image/jpeg"
            elif name.endswith(".png"): new_type = "image/png"
            
            if new_type:
                await client.patch(
                    f"{directus_url}/files/{f['id']}", 
                    json={"type": new_type}, 
                    headers=headers
                )

asyncio.run(main())
EOF

cd backend
uv run python ../seed_test_data.py
cd ..
rm seed_test_data.py
