# student-lms
---
## Launching
```
sudo docker compose up -d
```
```
sudo ./init-test-db.sh
```

In separate terminals:
- In first one
```
cd frontend
pnpm i
pnpm run dev
```
- In second one
```
cd backend
uv run alembic upgrade head
uv run uvicorn app.main:app --reload --port 8000
```
