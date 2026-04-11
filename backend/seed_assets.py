import os
import asyncio
import mimetypes
import httpx
from dotenv import load_dotenv

load_dotenv()

async def seed_assets():
    directus_url = os.getenv("DIRECTUS_URL", "http://localhost:8055")
    admin_email = os.getenv("DIRECTUS_ADMIN_EMAIL", "admin@example.com")
    admin_password = os.getenv("DIRECTUS_ADMIN_PASSWORD", "adminpassword")

    async with httpx.AsyncClient(timeout=30.0) as client:
        token = None
        for attempt in range(12):
            try:
                resp = await client.post(
                    f"{directus_url}/auth/login",
                    json={"email": admin_email, "password": admin_password}
                )
                if resp.status_code == 200:
                    token = resp.json()["data"]["access_token"]
                    print("Login successful")
                    break
            except Exception as e:
                print(f"Attempt {attempt+1}: connection error - {e}")
            await asyncio.sleep(5)

        if not token:
            print("Failed to obtain access token")
            return

        headers = {"Authorization": f"Bearer {token}"}
        assets_dir = "seed_data/assets"

        if not os.path.exists(assets_dir):
            print(f"Folder {assets_dir} not found, skipping file upload")
        else:
            print(f"Uploading files from {assets_dir}")
            for filename in os.listdir(assets_dir):
                filepath = os.path.join(assets_dir, filename)
                if not os.path.isfile(filepath):
                    continue

                check_res = await client.get(
                    f"{directus_url}/files",
                    params={"filter[filename_download][_eq]": filename},
                    headers=headers
                )
                if check_res.status_code == 200 and check_res.json().get("data"):
                    print(f"File {filename} already exists, skipping")
                    continue

                mime_type, _ = mimetypes.guess_type(filepath)
                if not mime_type:
                    mime_type = "application/octet-stream"

                with open(filepath, "rb") as f:
                    files = {"file": (filename, f, mime_type)}
                    upload_res = await client.post(
                        f"{directus_url}/files",
                        headers=headers,
                        files=files
                    )
                    if upload_res.status_code == 200:
                        print(f"Uploaded {filename}")
                    else:
                        print(f"Failed to upload {filename}: {upload_res.text}")

        print("Updating MIME types for uploaded files...")
        files_res = await client.get(f"{directus_url}/files", headers=headers)
        if files_res.status_code == 200:
            for file_item in files_res.json().get("data", []):
                name = file_item.get("filename_download", "")
                new_type = None
                if name.lower().endswith(".svg"):
                    new_type = "image/svg+xml"
                elif name.lower().endswith((".jpg", ".jpeg")):
                    new_type = "image/jpeg"
                elif name.lower().endswith(".png"):
                    new_type = "image/png"

                if new_type:
                    await client.patch(
                        f"{directus_url}/files/{file_item['id']}",
                        json={"type": new_type},
                        headers=headers
                    )
                    print(f"Updated type for {name} -> {new_type}")
        else:
            print("Failed to fetch files for type update")

if __name__ == "__main__":
    asyncio.run(seed_assets())
