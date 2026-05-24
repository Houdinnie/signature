# CLAUDE.md — Signature Autonomous AI Business OS

## What this project is
Signature is a self-hosted, autonomous AI platform that runs a company's operations 24/7. Nine specialized agents (Orchestrator, Planning, Competitor Research, Social Posts, Email Outreach, Support Reply, Ads, Code, Finance) run on a Celery + Redis task queue with a FastAPI backend and Next.js dashboard. Agents call the Claude Code CLI as a subprocess — no Anthropic API key is used.

## Running tests

cd backend
CLAUDE_CLI_MOCK=true python -m pytest tests/unit/ -v

With coverage:
CLAUDE_CLI_MOCK=true python -m pytest tests/unit/ --cov=app --cov-report=term-missing

Frontend:
cd frontend
npm test -- --watchAll=false

Integration:
cd backend
CLAUDE_CLI_MOCK=true python -m pytest tests/integration/ -v -m integration

## Key development commands
make up          # Start all Docker services
make down        # Stop
make migrate     # Run Alembic migrations
make seed        # Seed company config
make init-db     # migrate + seed
make lint        # ruff + mypy + eslint
make test        # unit + integration (via Docker)

## Architecture
FastAPI (sync, Python 3.12) serves the REST API. Celery workers pull tasks from Redis and run agents. Each agent inherits `BasePolsiaAgent` and calls `claude -p "..." --output-format json` as a subprocess. Results are written to PostgreSQL (SQLAlchemy, 17 tables) and semantic insights are dual-written to ChromaDB. Redis pub/sub broadcasts activity events to the WebSocket, which the Next.js dashboard consumes in real-time. `CLAUDE_CLI_MOCK=true` makes all agents return a stub response — used in all tests and CI.

## Critical env vars
CLAUDE_CLI_MOCK=true         # Always set in tests — skips real CLI subprocess
SANDBOX_MODE=true            # Prevents real API calls
API_KEY=dev-key              # X-API-Key header for dashboard API
DATABASE_URL=sqlite:///:memory:  # Unit tests use SQLite

## SQLite compatibility notes
All ORM models use `Text` (JSON) instead of `JSONB` or `ARRAY(String)` — this makes them work with SQLite in unit tests and PostgreSQL in production. Do not use PostgreSQL-specific dialect types.

## Model imports
`app/models/__init__.py` imports all models so Alembic can discover them. If you add a new model, import it there.

## Adding a new agent
1. Create `app/agents/<name>/agent.py` with a class inheriting `BasePolsiaAgent`
2. Add `"<name>": ("app.agents.<name>.agent", "<ClassName>")` to `AGENT_MAP` in `crew_factory.py`
3. Add the agent type string to `VALID_AGENT_TYPES` in `crew_factory.py`
4. Add a Beat schedule entry in `celery_app/beat_schedule.py` if periodic
5. Write unit tests in `tests/unit/test_<name>_agent.py`

## Adding a new API endpoint
1. Create `app/api/v1/<name>.py`
2. Register the router in `app/api/v1/api.py`
3. Write tests in `tests/unit/api/test_<name>.py`

## What CLAUDE_CLI_MOCK does
In `base_agent.py`, if `os.getenv("CLAUDE_CLI_MOCK")` is truthy, `call_claude()` returns the value of `CLAUDE_CLI_MOCK_RESPONSE` (defaults to `{"result": "Mock Claude response for testing"}`) instead of spawning a subprocess.

## Common pitfalls
- **Don't use PostgreSQL-specific types** — use `Text` for JSON fields, `Integer` for cents
- **Don't import `chromadb` at module level** — lazy-import inside functions
- **Money is always in cents** — `_cents` suffix on Integer columns, divide by 100 for display
- **Enum columns are strings** — use `String(50)` with validation in the service layer
- **Always patch where the name is used** — e.g. patch `app.services.memory_service.get_collection`
