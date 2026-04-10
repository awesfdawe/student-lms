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
source .venv/bin/activate
alembic upgrade head
uvicorn app.main:app --reload --port 8000
```
