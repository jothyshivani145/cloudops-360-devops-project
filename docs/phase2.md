# Phase 2 — Flask + PostgreSQL + Docker Compose

## Architecture
Browser --> localhost:5000 --> Gunicorn/Flask API --> PostgreSQL (Compose-only network)

## Local Python tests
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m pytest -q tests/test_app.py
```

## Run locally (SQLite for zero setup)
```bash
python -m flask --app app.wsgi:app run --host 127.0.0.1 --port 5000
```

## Run with Docker Compose + PostgreSQL
```bash
cp .env.example .env
# Edit .env to choose a local-only password. Keep it out of Git.
docker compose config
docker compose up --build -d
docker compose ps
curl http://127.0.0.1:5000/health
```
Visit http://localhost:5000 and create a ticket.

## CRUD API
- `GET /health` health + database check
- `GET /api/tickets` list
- `POST /api/tickets` create
- `PATCH /api/tickets/<id>` update status

## Maintenance
```bash
docker compose logs -f web
docker compose logs --tail 50 db
docker compose down
```
`docker compose down` keeps the named database volume. `docker compose down -v` **deletes the database volume and your tickets**.

## Important caveats
This is a local educational app. No authentication; do not expose it publicly. Flask's built-in server is for development, while the container uses Gunicorn. Table creation uses `db.create_all()` instead of migrations; add Alembic/Flask-Migrate before production deployment. Dependencies are version-ranged, not hash-locked; lock and scan them before production deployment.
