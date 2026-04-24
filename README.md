# student-lms
---
## Launching (dev)

You need to install the following dependencies: curl, jq, uv, and Docker with Docker Compose

```bash
sudo docker compose down -v --remove-orphans
```
```bash
sudo docker compose up -d 
```

In separate terminals:
- In first one
```bash
cd frontend
pnpm i
pnpm run dev
```
- In second one
```bash
cd backend
uv run alembic upgrade head
uv run uvicorn app.main:app --reload --port 8000
```
