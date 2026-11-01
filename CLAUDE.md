# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

All tooling goes through `uv`. Don't call `pip` directly. Python version is pinned in `.python-version`.

- First-time setup: `make env` (creates `.venv`, installs dev deps). `.github/copilot-instructions.md` calls this `make setup`, but that target doesn't exist.
- Dev server: `make start` (uvicorn with reload on 127.0.0.1:8000; OpenAPI docs at `/docs`)
- Tests: `make test`
- Single test: `uv run python -m pytest tests/test_todos.py::test_create_todo`
- Lint / format: `make lint` / `make format`. Both run `uv run ruff` so they use the version pinned in `requirements-dev.txt`. Don't switch them back to `uvx ruff`: that pulls the latest ruff, whose larger default rule set fails on this code.

CI (`.github/workflows/test.yml`) runs `make install-dev`, `make test` and `make lint`, then checks that `GET /` returns 200. Renovate keeps the pinned versions in `requirements*.txt`, the Makefile and the workflow up to date.

## Architecture

A small FastAPI CRUD API with three resources: users, posts and todos. It uses **raw SQL on SQLite (`sqlite3`), with no ORM**. Keep it that way.

- `app/main.py` registers the routers and configures CORS and docs based on `ENVIRONMENT`. It also calls `init_db()` at **import time** (not in a lifespan hook), so importing `app.main` creates the tables.
- `app/database.py` has `get_db()`, a context manager that opens a new connection per call. Writes need an explicit `db.commit()`. The schema lives in `init_db()` as `CREATE TABLE IF NOT EXISTS`. There are no migrations, so schema changes don't apply to an existing `data.db`.
- `app/routers/*.py` holds one `APIRouter(prefix="/<resource>", tags=[...])` per resource. Each endpoint calls `get_db()` directly; there is no FastAPI `Depends` injection. Handlers are plain `def` on purpose: `sqlite3` blocks, and FastAPI runs sync handlers in a threadpool. Don't make them `async def`.
- The API's only consumer is the SvelteKit app in `../JSONPlaceholderClient`. Its `src/types/*.ts` and `src/lib/api/*.ts` mirror these endpoints, so update them when you change the API.
- `app/models/*.py` holds Pydantic v2 models per resource: `XBase`, `XCreate`, `XUpdate` (all fields optional, for partial updates), plus a response model. Response model names vary: `User`, `Todo`, and `PostResponse`. `PostResponse` embeds a nested `author: User`, repeats the author's `userId` at the top level as a computed field, and treats `createdAt` as UTC (SQLite stores `CURRENT_TIMESTAMP` without a zone).

### Conventions and gotchas

- **Rows are read by positional index** (`row[0]`, `row[1]`, ...), often after `SELECT *`. If you add or reorder a column, update every construction site that indexes into rows.
- Partial updates build `UPDATE ... SET` dynamically from the non-`None` fields. Only column names that the code itself writes go into the f-string; values always go through `?` parameters.
- **Users have two IDs**: `id` (autoincrement int) and `userId` (a UUID string generated in `create_user`). The API paths (`/users/{userId}`) and `posts.userId` both use the UUID, not `id`.
- Foreign keys are declared but **not enforced**, because `PRAGMA foreign_keys` is never enabled. Routers check that the referenced user exists before inserting, and `delete_user` deletes the user's posts itself. Any new relationship needs the same manual handling.
- Email uniqueness is checked in router code (returns 400) as well as by the DB `UNIQUE` constraint.
- `PUT /todos/batch` must stay declared **before** `PUT /todos/{todo_id}` so that the route matches. The batch update runs as a single transaction: if any id is missing, it raises 404 before the commit.

## Configuration

These environment variables are read in `app/main.py` and `app/database.py`:

- `ENVIRONMENT=production`: turns off `/docs` and `/redoc`, limits CORS to `ALLOWED_ORIGINS` (comma-separated), and changes the default DB path to `/app/data/data.db`.
- `DATABASE_PATH`: overrides the DB location. The default in development is `data.db` in the current directory.

## Testing

Tests use FastAPI's `TestClient` through the `client` fixture in `tests/conftest.py`. Before `app.main` is imported, `conftest.py` sets `DATABASE_PATH` to a temporary file, so tests never touch the dev `data.db`. Keep `app.main` imported lazily inside fixtures. All tests in a session share that temp database, so each test module clears its tables with an autouse fixture; follow that pattern, since leftover users break the email-uniqueness checks.

## Deployment

The app deploys to Coolify via the `Dockerfile` (see `DEPLOYMENT.md`). The image is single-stage `python:3.14-alpine`, runs as root and serves on **port 80**; `make start-prod` uses 8000 instead. Mount a volume at `/app/data` so the SQLite file persists.
