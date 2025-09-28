## Monerating Backend (FastAPI)

FastAPI backend for Monerating: mood tracking, journaling, wearable data, alerts, and lightweight analytics.

### Features
- Users, mood logs, journal entries, wearable readings, and alerts
- CRUD REST endpoints
- SQLite by default; Postgres via Docker Compose
- Simple analytics: sentiment (VADER), trend slope, and anomaly detection

### Quickstart (Local)
1. Create a virtualenv and install deps:
   ```bash
   cd monerating_backend
   python3 -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. Run the API (uses SQLite by default):
   ```bash
   uvicorn app.main:app --reload
   ```
3. Open docs: `http://127.0.0.1:8000/docs`

### Environment
Copy `.env.example` to `.env` and adjust as needed. Defaults work for SQLite.

Key variables:
- `DATABASE_URL` – SQLAlchemy URL. Default: `sqlite:///./monerating.db`
- `APP_NAME` – Title shown in docs
- `APP_ENV` – `dev|prod`

### Docker (Postgres)
```bash
cp .env.example .env
docker compose up --build
```
API will be at `http://localhost:8000/docs` and Postgres on `localhost:5432`.

### Project Layout
```text
monerating_backend/
  app/
    core/            # configuration
    db/              # engine, session, base
    models/          # SQLAlchemy models
    routers/         # FastAPI routers (CRUD)
    schemas/         # Pydantic schemas
    services/        # analytics utilities
    main.py          # app entrypoint
  requirements.txt
  Dockerfile
  docker-compose.yml
  .env.example
  README.md
```

### Dev Tips
- The app will auto-create tables on start.
- Use `/analytics/*` routes for basic analysis.

### License
MIT

