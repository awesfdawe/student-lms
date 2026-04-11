#!/bin/bash

cat << 'EOF' > backend/.env
DIRECTUS_URL=http://localhost:8055
DIRECTUS_ADMIN_EMAIL=admin@example.com
DIRECTUS_ADMIN_PASSWORD=adminpassword
REDIS_URL=redis://127.0.0.1:6379
POSTGRES_SERVER=127.0.0.1
POSTGRES_PORT=5433
POSTGRES_USER=directus
POSTGRES_PASSWORD=directus_password
POSTGRES_DB=student_lms
SQLALCHEMY_DATABASE_URI=postgresql+asyncpg://directus:directus_password@127.0.0.1:5433/student_lms
WEBHOOK_SECRET=dev_secret_key
EOF

set -a
. backend/.env
set +a

cd backend
uv run alembic upgrade head || uv run alembic stamp head
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
        if login.status_code != 200:
            return
            
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

        flows = [
            {
                "name": "Sync Users",
                "icon": "sync",
                "color": "#2196F3",
                "trigger": "event",
                "status": "active",
                "options": {
                    "type": "action",
                    "scope": ["items.create", "items.update", "items.delete"],
                    "collections": ["users"]
                }
            },
            {
                "name": "Invalidate File Cache",
                "icon": "cached",
                "color": "#FFC107",
                "trigger": "event",
                "status": "active",
                "options": {
                    "type": "action",
                    "scope": ["items.create", "items.update", "items.delete"],
                    "collections": ["directus_files"]
                }
            },
            {
                "name": "FastAPI Cache Invalidation",
                "icon": "bolt",
                "color": "#6644FF",
                "trigger": "event",
                "status": "active",
                "options": {
                    "type": "action",
                    "scope": ["items.create", "items.update", "items.delete"],
                    "collections": [
                        "landing_page", 
                        "globals", 
                        "ui_dictionary", 
                        "pages", 
                        "courses", 
                        "faqs", 
                        "quiz"
                    ]
                }
            }
        ]

        for flow_payload in flows:
            flow_res = await client.get(f"{directus_url}/flows?filter[name][_eq]={flow_payload['name']}", headers=headers)
            if flow_res.status_code == 200 and not flow_res.json().get("data"):
                create_flow = await client.post(f"{directus_url}/flows", headers=headers, json=flow_payload)
                if create_flow.status_code == 200:
                    flow_id = create_flow.json()["data"]["id"]
                    op_payload = {
                        "name": "Call Webhook",
                        "key": "call_webhook",
                        "type": "webhook",
                        "position_x": 1,
                        "position_y": 1,
                        "flow": flow_id,
                        "options": {
                            "method": "POST",
                            "url": "http://host.docker.internal:8000/api/webhooks/directus_update",
                            "payload": '{"collection": "{{$trigger.collection}}", "event": "{{$trigger.event}}", "payload": {}}'
                        }
                    }
                    await client.post(f"{directus_url}/operations", headers=headers, json=op_payload)

asyncio.run(main())
EOF

cd backend
uv run python seed.py
cd ..
rm seed_test_data.py
