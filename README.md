# AI Backend System — Microservices

A fraud-detection backend built as independent FastAPI microservices behind an nginx gateway,
orchestrated with Docker Compose. The `ai-service` scores a transaction for fraud and fans out
to the other services for geo-enrichment, alerting, and logging.

## Services

| Service                | Internal port | Responsibility |
|------------------------|---------------|----------------|
| `gateway`              | 80 (→ host 8080) | nginx reverse proxy; routes by path prefix |
| `user-service`         | 8001 | Signup/login, bcrypt password hashing, JWT issuance (Postgres) |
| `ai-service`           | 8002 | Fraud scoring orchestrator (`POST /fraud/predict`) |
| `alert-service`        | 8003 | Receives fraud alerts (`POST /alert/`) |
| `log-service`          | 8004 | Ingests/returns structured logs (`/logs/`) |
| `external-api-service` | 8005 | GeoIP lookups via ipinfo.io (`GET /geoip/{ip}`) |

Each service follows the same layering under `<service>/app/`: `main.py` (FastAPI app) →
`routes/` → `services/` (business logic) → `repositories/` / `database/`, with `models.py`
(SQLAlchemy) and `schemas.py` (Pydantic).

## Request flow

`POST /fraud/predict` on `ai-service`:
1. If an `ip` is supplied, calls `external-api-service` `/geoip/{ip}` to resolve a city.
2. Encodes features and runs `FraudModel` (loads `model_files/fraud_model.pkl` if present,
   otherwise falls back to mock threshold logic — the model file is not committed).
3. Concurrently notifies `alert-service` `/alert/` and `log-service` `/logs/`.

Services talk to each other over the Docker `backend` network using their internal ports
(e.g. `http://alert-service:8003/alert/`).

## Running

```bash
cp .env.example .env      # then fill in real values
docker-compose up --build
```

The gateway is then reachable at `http://localhost:8080` (e.g. `POST /fraud/predict`,
`POST /user/signup`). Individual services are also published on their ports above.

To run a single service locally:

```bash
cd <service>
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port <port> --reload
```

## Configuration

`DATABASE_URL` is **required** and read only from the environment — there is no hardcoded
fallback, so a service raises `RuntimeError` at import if it is unset. Per-service values live in
`.env` (gitignored) and are injected by docker-compose; see `.env.example` for the template. For
local runs outside Docker, export `DATABASE_URL` yourself (e.g. `$env:DATABASE_URL = "..."`).
`JWT_SECRET_KEY` is also read from the environment (it keeps a default so existing tokens work).
