# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

A fraud-detection backend built as five independent FastAPI microservices plus an nginx
gateway, orchestrated with Docker Compose. The `ai-service` is the orchestrator: it scores a
transaction for fraud and fans out to the other services for geo-enrichment, alerting, and
logging.

## Commands

Everything runs through Docker Compose — there is no top-level test suite or build script.

```bash
docker-compose up --build          # build images and start all services
docker-compose up ai-service       # start one service (and its depends_on chain)
docker-compose logs -f ai-service  # tail one service's logs
docker-compose down                # stop everything
```

Each service can also run standalone (uvicorn is invoked with `--reload`, so code edits
hot-reload inside the container). From a service directory:

```bash
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port <service-port> --reload
```

There are currently **no tests, linters, or formatters configured**. `ai_service/venv/` is a
checked-in virtualenv — do not edit files under any `venv/` directory.

## Architecture

Each service is a self-contained FastAPI app under `<service>/app/` following the same layering:

- `main.py` — creates the `FastAPI()` app and includes routers
- `routes/` — HTTP endpoints; thin, delegate to services
- `services/` — business logic
- `repositories/` — data-access layer (only `user_service` uses this)
- `models.py` — SQLAlchemy ORM models; `schemas.py` — Pydantic request/response models
- `database/database.py` — SQLAlchemy engine/session, one per service

Dependencies are wired with FastAPI's `Depends`. `user_service` is the cleanest example of the
intended pattern: route → `UserService` → `user_repository` → DB session injected via `get_db`.

### Service responsibilities and ports

The uvicorn `CMD` port in each Dockerfile is the **internal** port other services must call.

| Service                | Internal port (Dockerfile CMD) | Role |
|------------------------|--------------------------------|------|
| `user-service`         | 8001 | Signup/login, bcrypt hashing, JWT issuance (Postgres `users` DB) |
| `ai-service`           | 8002 | Fraud scoring orchestrator (`POST /fraud/predict`) |
| `alert-service`        | 8003 | Receives alerts (`POST /alert/`), currently just logs them |
| `log-service`          | 8004 | Ingests structured logs (`POST /logs/`); S3 persistence is stubbed out |
| `external-api-service` | 8005 | GeoIP lookups via ipinfo.io (`GET /geoip/{ip}`) |

### Request flow (the core path)

`ai-service` `POST /fraud/predict` (`prediction_service.py`):
1. If an `ip` is provided, calls `external-api-service` `/geoip/{ip}` to resolve a city.
2. Encodes features and runs `FraudModel.predict` (loads `app/model_files/fraud_model.pkl` if
   present, otherwise falls back to mock threshold logic — the model file is **not** in the repo).
3. Fans out concurrently with `asyncio.gather` to `alert-service` `/alert/` and
   `log-service` `/logs/`.

Inter-service calls use `httpx.AsyncClient` against Docker DNS names on the `backend` network
(e.g. `http://alert-service:8003/alert/`). These calls hit the **internal** Dockerfile CMD port,
not the host-published port.

## Configuration & conventions

- **`DATABASE_URL` is required and env-only.** Each `app/database/database.py` does
  `os.getenv("DATABASE_URL")` with **no hardcoded fallback** and raises `RuntimeError` at import if
  it is unset. docker-compose injects it per service from root `.env` (`USER_DATABASE_URL`,
  `AI_DATABASE_URL`, etc. → `DATABASE_URL`). For local non-Docker runs, export `DATABASE_URL`
  yourself. The real AWS RDS values live in `.env`, which is **gitignored and untracked** — never
  re-add credentials to source. The credentials remain in older git history (pre-cleanup), so they
  should be rotated in AWS.
- `JWT_SECRET_KEY` is read via `os.getenv("JWT_SECRET_KEY", "supersecretkey")` — env-overridable
  but keeps a default so existing tokens validate.

## Known quirks to be aware of

- **Two port numbering systems.** Each service's Dockerfile `CMD` port (8001 user, 8002 ai,
  8003 alert, 8004 log, 8005 external-api) is the *internal* port other services and the gateway
  must call; `docker-compose.yml` publishes those same numbers to the host. Inter-service URLs in
  `prediction_service.py` and `gateway/nginx.conf` target the internal ports — keep all three in
  sync when changing a port.
- **`log-service` persistence is in-memory**, not S3. `LogService` keeps a shared class-level list
  (`GET /logs/` returns it); swap `_store.append` for an S3 `put_object` when a bucket exists.
- **`ai-service` model file is not committed.** `FraudModel` loads `model_files/fraud_model.pkl`
  if present, otherwise uses mock threshold logic. `model_files/` holds only a `.gitkeep` so the
  Dockerfile `COPY` succeeds.
- `deploy/`, `redis/`, and `shared/` are empty placeholder directories.
