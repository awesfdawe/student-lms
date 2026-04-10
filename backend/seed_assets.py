import os
import httpx
import asyncio

async def seed_assets():
    async with httpx.AsyncClient() as client:
        login_data = {"email": "admin@example.com", "password": "adminpassword"}
        token = None
        for _ in range(12):
            try:
                res = await client.post("http://directus:8055/auth/login", json=login_data)
                if res.status_code == 200:
                    token = res.json()["data"]["access_token"]
                    break
            except Exception:
                pass
            await asyncio.sleep(5)
        
        if not token:
            return

        headers = {"Authorization": f"Bearer {token}"}
        assets_dir = "seed_data/assets"
        
        if os.path.exists(assets_dir):
            for filename in os.listdir(assets_dir):
                filepath = os.path.join(assets_dir, filename)
                if not os.path.isfile(filepath):
                    continue
                    
                check_res = await client.get(f"http://directus:8055/files?filter[filename_download][_eq]={filename}", headers=headers)
                if check_res.status_code == 200 and not check_res.json()["data"]:
                    with open(filepath, "rb") as f:
                        await client.post(
                            "http://directus:8055/files",
                            headers=headers,
                            files={"file": (filename, f, "application/octet-stream")}
                        )

        flow_payload = {
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
        }
        
        flows_res = await client.get("http://directus:8055/flows?filter[name][_eq]=Invalidate File Cache", headers=headers)
        flow_id = None
        if flows_res.status_code == 200 and not flows_res.json()["data"]:
            flow_create = await client.post("http://directus:8055/flows", headers=headers, json=flow_payload)
            if flow_create.status_code == 200:
                flow_id = flow_create.json()["data"]["id"]
        elif flows_res.status_code == 200:
            flow_id = flows_res.json()["data"][0]["id"]
            
        if flow_id:
            op_payload = {
                "name": "Call Webhook",
                "key": "call_webhook",
                "type": "webhook",
                "position_x": 1,
                "position_y": 1,
                "flow": flow_id,
                "options": {
                    "method": "POST",
                    "url": "http://backend:8000/api/webhooks/directus_update",
                    "payload": '{"collection": "directus_files", "event": "{{$trigger.event}}", "payload": {}}'
                }
            }
            ops_res = await client.get(f"http://directus:8055/operations?filter[flow][_eq]={flow_id}", headers=headers)
            if ops_res.status_code == 200 and not ops_res.json()["data"]:
                await client.post("http://directus:8055/operations", headers=headers, json=op_payload)

if __name__ == "__main__":
    asyncio.run(seed_assets())
